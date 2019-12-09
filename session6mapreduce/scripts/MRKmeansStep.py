"""
.. module:: MRKmeansDef

MRKmeansDef
*************

:Description: MRKmeansDef

    

:Authors: bejar
    

:Version: 

:Created on: 17/07/2017 7:42 

"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import Counter

__author__ = 'bejar'


class MRKmeansStep(MRJob):
    prototypes = {}

    def jaccard(self, prot, doc):
        """
        Compute here the Jaccard similarity between  a prototype and a document
        prot should be a list of pairs (word, probability)
        doc should be a list of words
        Words must be alphabeticaly ordered

        The result should be always a value in the range [0,1]
        """
        dot_product = 0
        i = j = 0
        while i < len(prot) and j < len(doc):
            if prot[i][0] < doc[j]:
                i+=1
            elif doc[j] < prot[i][0]:
                j+=1
            else:
                dot_product += 1
                i += 1
                j += 1
        union = len(prot) + len(doc)
        return (dot_product / (union - dot_product) )

    def configure_args(self):
        """
        Additional configuration flag to get the prototypes files

        :return:
        """
        super(MRKmeansStep, self).configure_args()
        self.add_file_arg('--prot')

    def load_data(self):
        """
        Loads the current cluster prototypes

        :return:
        """
        f = open(self.options.prot, 'r')
        for line in f:
            cluster, words = line.split(':')
            cp = []
            for word in words.split():
                cp.append((word.split('+')[0], float(word.split('+')[1])))
            self.prototypes[cluster] = cp

    def assign_prototype(self, _, line):
        """
        This is the mapper it should compute the closest prototype to a document

        Words should be sorted alphabetically in the prototypes and the documents

        This function has to return at list of pairs (prototype_id, document words)

        You can add also more elements to the value element, for example the document_id
        """

        # Each line is a string docid:wor1 word2 ... wordn
        doc, words = line.split(':')
        lwords = words.split()
        
        #
        # Expectation:
        #   Computar la similitud del document amb tots els
        #   prototypes, guanya el prototype amb mes similitud
        #
        
        max_sim = -1
        prototype_id = ""
        for prot in self.prototypes:
            sim = self.jaccard(self.prototypes[prot], lwords) 
            if max_sim < sim:
                max_sim = sim
                prototype_id = prot


        # Return pair key, value
        yield prototype_id, (doc, lwords)

    def aggregate_prototype(self, key, values):
        """
        input is cluster and all the documents it has assigned
        Outputs should be at least a pair (cluster, new prototype)

        It should receive a list with all the words of the documents assigned for a cluster

        The value for each word has to be the frequency of the word divided by the number
        of documents assigned to the cluster

        Words are ordered alphabetically but you will have to use an efficient structure to
        compute the frequency of each word

        :param key:
        :param values:
        :return:
        """
        computed_words = {}
        ndocs = 0
        docs = []
        for doc in values:
            docs.append(doc[0])
            ndocs += 1
            occurs = dict(Counter(doc[1])) # retorna un diccionari word : occurrencies
            for word in occurs:
                if word not in computed_words:
                    computed_words[word] = occurs[word]
                else:
                    computed_words[word] += occurs[word]
        # Genera un cluster associat a una llista de documents amb un prototip de la forma list (token, norm_freq)
        #tokens = map(lambda x: (x[0], x[1]/ndocs), sorted(computed_words.items()))
        tokens = []
        for doc in sorted(computed_words.items()):
            tokens.append((doc[0], doc[1]/ndocs))
        yield key, (sorted(docs), tokens)

    def steps(self):
        return [MRStep(mapper_init=self.load_data, mapper=self.assign_prototype,
                       reducer=self.aggregate_prototype)
            ]


if __name__ == '__main__':
    MRKmeansStep.run()
