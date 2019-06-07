# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:48:58 2019

@author: Valentin
"""
from Permutation import Permutation

class TabuSearch:
    def __init__(self,taixxa):
        self._perm = Permutation(taixxa._modulesNumber)
        self._data = taixxa
        
    def tabuSearch(self, maxIter, lenList):
        self._perm.shuffle()
        fitness = []
        xmin = self._perm
        fmin = self._perm.computeCost(self._data)
        T = []
        for i in range(maxIter):
            Txi = list(map(lambda x: self._perm.permute(x[0],x[1]), T))
            C = [x for x in self._perm.getNeighbours() if x not in Txi]
            fC = list(map(lambda x: x.computeCost(self._data), C))
            xnext = C[fC.index(min(fC))]
            variationF = xnext.computeCost(self._data) - self._perm.computeCost(self._data)
            if variationF >= 0:
                if T.count(xnext.reversePerm(self._perm)) == 0:
                    T.append(xnext.reversePerm(self._perm))
                if len(T) > lenList:
                    T.pop(0)
            fnext = xnext.computeCost(self._data)
            if fnext < fmin:
                xmin = xnext
                fmin = fnext
            self._perm = xnext
            fitness.append(self._perm.computeCost(self._data))
        return xmin, fitness