# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:33:55 2019

@author: Valentin
"""
import random as rd
import numpy as np
import copy
from Permutation import Permutation

class SimulatedAnnealing:
    
    def __init__(self,taixxa):
        self._perm = Permutation(taixxa._modulesNumber)
        self._data = taixxa
        
    def solve(self, t0, mu, n1, n2, f):
        self._perm.shuffle()
        fitness = []
        i = 0
        xmin = self._perm
        xnext = 0
        temp = t0
        temps =[t0]
        fmin = self._perm.computeCost(self._data)
        fitness.append(fmin)
        for k in range(n1):
            neighbours = self._perm.getNeighbours()
            # print(neighbours)
            for l in range(1, n2):
                y = rd.choice(neighbours)
                variationF = y.computeCost(self._data) - self._perm.computeCost(self._data)
                if variationF <= 0:
                    xnext = y
                    fnext = xnext.computeCost(self._data)
                    if fnext < fmin:
                        xmin = xnext
                        fmin = fnext
                else:
                    p = rd.uniform(0, 1)
                    if p <= np.exp(-variationF / temp):
                        xnext = y
                    else:
                        xnext = self._perm
                self._perm = xnext
                
                fitness.append(self._perm.computeCost(self._data))
            i = i+1
            temp = f(t0,i)
            temps.append(temp)
        return copy.deepcopy(xmin), np.array(fitness), np.array(temps)