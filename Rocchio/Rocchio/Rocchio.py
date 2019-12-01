"""
.. module:: SearchIndexWeight

Rocchio
*************

:Description: Roochio

    Performs a AND query for a list of words (--query) in the documents of an index (--index)
    You can use word^number to change the importance of a word in the match

    --nhits changes the number of documents to retrieve

:Authors:
    Diego Delgado
    Oriol Vidal

:Version:
    666
:Created on: 30/10/2019

"""

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse
import numpy as np
import bisect

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch.client import CatClient

__author__ = 'DDED'
def mutableQuery2Array (mutableQuery):
    '''
    Pasa de un array de tuplas (términos, pesos) a un array de "términos^pesos"
    '''
    query = []
    for subMutableQuery in mutableQuery:
        query.append(subMutableQuery[0]+"^"+str(subMutableQuery[1]))
    return query

def getMutableQuery(query):
    '''
    Pasa de un array de "términos^pesos" a un array de de tuplas(términos, pesos)
    '''
    mutableQuery = []
    for subQuery in query:
        mutableSubQuery = subQuery.split("^")
        if len(mutableSubQuery) == 1:
            mutableQuery.append((mutableSubQuery[0], 1))
        else:
            mutableQuery.append((mutableSubQuery[0], int(mutableSubQuery[1])))
    return mutableQuery

def doc_count(client, index):
    """
    Returns the number of documents in an index
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)
    file_td = {}
    file_df = {}
    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())

def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document
    """
    # Get document terms frequency and overall terms document frequency
    file_tv, file_df = document_term_vector(client, index, file_id)
    max_freq = max([f for _, f in file_tv])
    dcount = doc_count(client, index)
    tfidfw = []
    for (t, w),(_, df) in zip(file_tv, file_df):
        tf = w / max_freq
        idf = np.log2(dcount/df)
        weight = tf * idf
        tfidfw.append((t,weight))
    return normalize(tfidfw)

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    """
    sumw = 0
    for (_,w) in tw:
        sumw += w**2
    norm = np.sqrt(sumw)
    tw = [(t,w/norm) for (t,w) in tw]
    return tw

def queryAux(s, mutableQuery, k):
    '''
    Para simplificar la llamada a la query se ha dejado resumida en una función
    '''
    query = mutableQuery2Array(mutableQuery)
    q = Q('query_string',query=query[0])
    for i in range(1, len(query)):
        q &= Q('query_string',query=query[i])
    s = s.query(q)
    response = s[0:k].execute()
    relevantDocsIndex = []
    paths = []
    for r in response:  # only returns a specific number of results
        relevantDocsIndex.append(r.meta.id)
        paths.append(r.path)
    print(paths)
    return(relevantDocsIndex)

def add_weight (l,term,weight):
    '''
    Añade un término a la lista ordenada por pesos y elimina el de menos peso
    '''
    del l[0]
    lo = 0
    hi = len(l)
    while lo < hi:
        mid = (lo+hi)//2
        if weight < l[mid][1]: hi = mid
        else: lo = mid+1
    l.insert(lo, (term,weight))

def getRRelevantTerms(termsDictionary, R):
    '''
    Consigue los R términos relevantes a partir del diccionario[términos] = pesos
    '''
    size = 0
    newMutableSubQuery = []
    # se crea un array de tuplas(término, peso) de tamaño R
    for term in termsDictionary:
        if size == R:
            break
        else:
            size +=1
            newMutableSubQuery.append((term, termsDictionary[term]))
            # no se pueden los elementos de un dictionary iterando, así que modifico los valores a -1
            termsDictionary[term] = -1
    # se ordena por peso
    newMutableSubQuery = sorted(newMutableSubQuery, key = lambda x:x[1])

    for term in termsDictionary:
        if termsDictionary[term]>newMutableSubQuery[0][1]:
            add_weight(newMutableSubQuery, term, termsDictionary[term])
    return newMutableSubQuery
def rocchio(index, client, s, mutableQuery,k,nrounds,R, alpha, beta):
    for _ in range(nrounds):
        relevantDocsIndex = queryAux(s, mutableQuery, k)
        termsDictionary = {}
        for relevantDocIndex in relevantDocsIndex:
            # suma los pesos de los términos comunes del vector tfidf
            for weightTerm in toTFIDF(client, index, relevantDocIndex):
                if weightTerm[0] in termsDictionary:
                    termsDictionary[weightTerm[0]] += beta*weightTerm[1]/k
                else:
                    termsDictionary[weightTerm[0]] = beta*weightTerm[1]/k
        for mutableSubQuery in mutableQuery:
            # suma los pesos de la query actual
            if mutableSubQuery[0] in termsDictionary:
                termsDictionary[mutableSubQuery[0]] += alpha*mutableSubQuery[1]
            else:
                termsDictionary[mutableSubQuery[0]] = alpha*mutableSubQuery[1]
        mutableQuery = getRRelevantTerms(termsDictionary, R)
    # print para debugar la salida de cada iteración del bucle
        #print(mutableQuery)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nrounds', default=15, type=int, help='Number of rounds to execute Rocchio')
    parser.add_argument('--k', default=20, type=int, help='Number of relevant documents to return')
    parser.add_argument('--R', default=500, type=int, help='Number of relevant terms to search')
    parser.add_argument('--alpha', default=0.9, type=float, help='Number of relevant terms to search')
    parser.add_argument('--beta', default=0.1, type=float, help='Number of relevant terms to search')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')
    args = parser.parse_args()

    index = args.index
    query = args.query
    nrounds = args.nrounds
    R = args.R
    alpha = args.alpha
    beta = args.beta
    k = args.k
    mutableQuery = getMutableQuery(query)
    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if mutableQuery is not None:
            rocchio(index ,client, s, mutableQuery, k, nrounds, R, alpha, beta)
        else:
            print('No query parameters passed')

    except NotFoundError:
        print(f'Index {index} does not exists')

