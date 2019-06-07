import numpy as np
import random as rd
import sys
from Permutation import Permutation
import pickle

class Taixxa:

    def __init__(self):
        self._weights = []
        self._distances = []
        self._perm = Permutation(0)
        self._modulesNumber = 0
        self._hashMap = {}
        self._access = 0
        self._filename = ""

    def loadFile(self, filename):

        self._filename = filename
        with open(filename, "r") as f:
            lines = f.readlines()
            
            self._modulesNumber = int(lines[0])
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[1:self._modulesNumber + 1]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self._weights = np.array(temp[:])
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[self._modulesNumber + 2:]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self._distances = np.array(temp[:-1])

        
        self.loadHashMap()
        self._perm = Permutation(modulesNumber=self._modulesNumber)
        self._perm.shuffle()
        print(self._perm._perm)

    def addHash(self,hashed,cost):
        self._hashMap[hashed] = cost
    
    def getCost(self,hashed):
        self._access += 1
        return self._hashMap[hashed]
    
    def saveHashMap(self):
        with open(self._filename+'.hash' , 'wb') as f:
            pickle.dump(self._hashMap,f)
            
    def loadHashMap(self):
        try:
            with open(self._filename+'.hash' , 'rb') as f:
                self._hashMap = pickle.load(f)
        except FileNotFoundError:
            print("file hash not yet created think about saving for next time")
        

    # TODO Neighbourhood of n distance ?
    
        
        
