#!/usr/bin/python

from collections import namedtuple
import time
import sys
import math
import operator

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routeHash = dict() # totes les rutes d'un aeroport j a "self"
        self.outweight = 0   # write appropriate value

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

pageRanks = dict()

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    midal=0
    midad=0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            # no afegim l'aeroport si aquest te un IATA duplicat
            if a.code not in airportHash:
                cont += 1
                airportList.append(a)
                airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readlines():
        temp = line.split(',')
        # descartem la ruta si conte algun aeroport que no esta a V
        if not (temp[2] not in airportHash or temp[4] not in airportHash):
            # augmentem el nombre d'arestes de sortida del node "origen"
            airportHash[temp[2]].outweight += 1
            # mirem si el node desti te alguna aresta del node origen
            if temp[2] in airportHash[temp[4]].routeHash:
                airportHash[temp[4]].routeHash[temp[2]].weight += 1
            else:
                # creem una aresta amb origen "aeroport origen"
                r = Edge(temp[2])
                cont += 1
                # posem aquesta aresta a la llista d'arestes que apunten a "desti"
                airportHash[temp[4]].routeHash[temp[2]] = r
    routesTxt.close()
    print("There were {0} Routes with IATA code".format(cont))



def computePageRanks():
    global pageRanks
    n = len(airportList)
    L = 0.85
    error = 1e-6
    P = {(a.code):(1/n) for a in airportList}
    iterations = int(math.log(error, 10) / math.log(L, 10))
    # obtenim els nodes que no tenen arestes de sortida
    deadNodes = [v.code for v in airportList if v.outweight == 0]
    # print("#deadNodes =", len(deadNodes))
    # print("#airports with no incoming routes =", len([a for a in airportHash if
    #    len(airportHash[a].routeHash) == 0]))
    for it in range(iterations):
        # gestionem el problema dels nodes sense arestes de sorida
        sumDeadNodes = sum([(P[v]/n) for v in deadNodes])
        Q = {(a.code):0 for a in airportList}
        # Per a tot aeroport i
        for i in list(airportHash.keys()):
            suma = 0
            # Per a tot aeroport j que apunta a i
            for j in airportHash[i].routeHash:
                suma += (P[j] * airportHash[i].routeHash[j].weight) / airportHash[j].outweight
            Q[i] = L * (suma + sumDeadNodes) + ((1 - L)/n)
        P = Q 
    pageRanks = P
    # print("sum of pageranks =", sum(list(pageRanks.values())))
    return iterations

def outputPageRanks():
    pg_sorted = sorted(pageRanks.items(), key=operator.itemgetter(1))
    pg_sorted.reverse()
    for elem in pg_sorted:
        print((airportHash[elem[0]].name, elem[1]))
    print("sum of pageranks =", sum(list(pageRanks.values())))

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
