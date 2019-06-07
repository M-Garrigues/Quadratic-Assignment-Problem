import numpy as np
import random as rd
import sys
sys.path.insert(0, '../src/model/')
from Permutation import Permutation


class Taixxa:

    def __init__(self):
        self.weights = []
        self.distances = []
        self.permutation = Permutation(0)
        self.modulesNumber = 0

    def loadFile(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()
            
            self.modulesNumber = int(lines[0])
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[1:self.modulesNumber + 1]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self.weights = np.array(temp[:])
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[self.modulesNumber + 2:]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self.distances = np.array(temp[:-1])

        self.permutation = Permutation(modulesNumber=self.modulesNumber)
        self.permutation.shuffle()
        print(self.permutation._perm)


    

    # TODO Neighbourhood of n distance ?
    

    def simulatedAnnealing(self, t0, mu, n1, n2):
        fitness = []
        xmin = self.permutation
        xnext = 0
        temp = t0
        fmin = self.permutation.computeCost(self)
        fitness.append(fmin)
        for k in range(n1):
            neighbours = self.permutation.getNeighbours()
            # print(neighbours)
            for l in range(1, n2):
                y = rd.choice(neighbours)
                variationF = y.computeCost(self) - self.permutation.computeCost(self)
                if variationF <= 0:
                    xnext = y
                    fnext = xnext.computeCost(self)
                    if fnext < fmin:
                        xmin = xnext
                        fmin = fnext
                else:
                    p = rd.uniform(0, 1)
                    if p <= np.exp(-variationF / temp):
                        xnext = y
                    else:
                        xnext = self.permutation
                self.permutation = xnext
                fitness.append(self.permutation.computeCost(self))
            temp = temp * mu
        return xmin, fitness

    # TODO séparer les data et les résolutions + besoin d'un objet permutation pour simplifier le tabu search (actuellement ce n'est pas la vrai version de l'algo)
    def tabuSearch(self, maxIter, lenList):
        fitness = []
        xmin = self.permutation
        fmin = self.permutation.computeCost(self)
        T = []
        for i in range(maxIter):
            Txi = list(map(lambda x: self.permutation.permute(x[0],x[1]), T))
            C = [x for x in self.permutation.getNeighbours() if x not in Txi]
            fC = list(map(lambda x: x.computeCost(self), C))
            xnext = C[fC.index(min(fC))]
            variationF = xnext.computeCost(self) - self.permutation.computeCost(self)
            if variationF >= 0:
                if T.count(xnext.reversePerm(self.permutation)) == 0:
                    T.append(xnext.reversePerm(self.permutation))
                if len(T) > lenList:
                    T.pop(0)
            fnext = xnext.computeCost(self)
            if fnext < fmin:
                xmin = xnext
                fmin = fnext
            self.permutation = xnext
            fitness.append(self.permutation.computeCost(self))
        return xmin, fitness
