import random as rd
import copy

class Permutation:

    
    def __init__(self,modulesNumber,perm=None):
        if(perm != None):
            self._perm = perm
        else:
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
    
    def permhash(self):
        prehash = tuple(self._perm)
        return hash(prehash)
        
    
    def computeCost(self, taixxa):
        newCost = 0
        hashed = self.permhash()
        if  hashed in taixxa._hashMap:
            return taixxa.getCost(hashed)
        else:
            for i in range(len(self._perm)):
                for j in range(i,len(self._perm)):
                    newCost += taixxa._weights[i, j] * taixxa._distances[self._perm[i], self._perm[j]]
        taixxa.addHash(hashed,newCost)
        return newCost
    
    def reversePerm(self,permutation):
        both = set(permutation._perm).intersection(self._perm)
        return [permutation._perm.index(x) for x in both]
        

    def get(self, i):
        return self._perm[i]

    def set(self, i, val):
        self._perm[i] = val
        
    def setAll(self, perm):
        self._perm = perm
        
