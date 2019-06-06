import numpy as np
import random as rd


class Taixxa:

    def __init__(self):
        self.weights = np.array([])
        self.distances = np.array([])
        self.permutation = np.array([])
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
            
        self.permutation = list(range(self.modulesNumber))


    def computeCost(self, perm=None):
        newCost = 0
        if perm is None:
            perm = self.permutation
        for i in range(self.modulesNumber):
            for j in range(self.modulesNumber):
                newCost += self.weights[i, j] * self.distances[perm[i], perm[j]]
        return newCost
    
#TODO Neighbourhood of n distance ?
    def getNeighbours(self):
        neighbours = []
        for i in range(self.modulesNumber):
            for j in range(i, self.modulesNumber):
                if i != j:
                    temp = self.permutation[:]
                    temp[i] = self.permutation[j]
                    temp[j] = self.permutation[i]
                    # print(temp)
                    neighbours.append(temp)
        return neighbours

    def simulatedAnnealing(self, t0, mu,n1 ,n2):
        fitness = []
        xmin = self.permutation
        xnext = 0
        temp = t0
        fmin = self.computeCost()
        fitness.append(fmin)
        for k in range(n1):
            neighbours = self.getNeighbours()
            # print(neighbours)
            for l in range(1, n2):
                y = rd.choice(neighbours)
                variationF = self.computeCost(y) - self.computeCost()
                if variationF <= 0:
                    xnext = y
                    fnext = self.computeCost(xnext)
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
                fitness.append(self.computeCost())
            temp = temp * mu
        return xmin, fitness
    
    
    # TODO séparer les data et les résolutions + besoin d'un objet permutation pour simplifier le tabu search (actuellement ce n'est pas la vrai version de l'algo)
    def tabuSearch(self,maxIter, lenList):
        fitness = []
        xmin = self.permutation
        fmin = self.computeCost()
        T = []
        for i in range(maxIter):
            C = [x for x in self.getNeighbours() if x not in T]
            fC = list(map(lambda x: self.computeCost(x),C))
            xnext = C[fC.index(min(fC))]
            variationF = self.computeCost(xnext) - self.computeCost()
            if variationF >= 0:
                T.append(xnext)
                if len(T) > lenList:
                    T.pop(0)
            fnext = self.computeCost(xnext)
            if fnext < fmin:
                xmin = xnext
                fmin = fnext
            self.permutation = xnext
            fitness.append(self.computeCost())
        return xmin ,fitness
            
                      
            
            
            