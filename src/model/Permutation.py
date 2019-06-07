import random as rd
import copy

class Permutation:

    def __init__(self, modulesNumber):
        self._perm = list(range(modulesNumber))
        self._cost = 0

    def __getitem__(self, item):
        return self._perm[item]

    def shuffle(self):
        rd.shuffle(self._perm)
    
    def permute(self, i, j):
        tmp = self._perm[i]
        self._perm[i] = self._perm[j]
        self._perm[j] = tmp
        
    def getNeighbours(self):
        neighbours = []
        for i in range(len(self._perm)):
            for j in range(i,len(self._perm)):
                if i != j:
                    temp = copy.deepcopy(self)
                    temp.permute(i,j)
                    neighbours.append(temp)
        return neighbours
        
    def computeCost(self, taixxa):
        newCost = 0
        for i in range(len(self._perm)):
            for j in range(i,len(self._perm)):
                newCost += taixxa.weights[i, j] * taixxa.distances[self._perm[i], self._perm[j]]
        return newCost
    
    def reversePerm(self,permutation):
        both = set(permutation._perm).intersection(self._perm)
        return [permutation._perm.index(x) for x in both]
        

    def get(self, i):
        return self._perm[i]

    def set(self, i, val):
        self._perm[i] = val
