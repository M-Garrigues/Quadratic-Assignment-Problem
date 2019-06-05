import numpy as np
import random as rd


class Taixxa:

    def __init__(self):
        weights = []
        distances = []
        permutation = []
        cost = 0
        modulesNumber = 0

    def loadFile(self, filename):

        with open(filename, "r") as f:
            lines = f.readlines()
            self.modulesNumber = int(lines[0])
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[2:self.modulesNumber + 2]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self.weights = np.array(temp)
            temp = list(map(lambda x: list(filter(lambda a: a != '', x)),
                            list(map(lambda x: x[:-1].split(" "), lines[self.modulesNumber + 3:len(lines)]))))
            temp = list(map(lambda x: list(map(lambda a: int(a), x)), temp))
            self.distances = np.array(temp)

        self.permutation = list(range(self.modulesNumber))
        print(self.permutation)

    def computeCost(self, perm=None):
        newCost = 0
        if perm is None:
            perm = self.permutation
        for i in range(self.modulesNumber):
            for j in range(self.modulesNumber):
                newCost += self.weights[i, j] * self.distances[perm[i], perm[j]]
        return newCost

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

    # TODO Ajouter fonction pour varier la manière dont la température décroit
    # TODO Mettre tous les paramètres initaux en paramètres
    # TODO Ajouter une mémoire du fitness à chaque itération
    def simulatedAnnealing(self, t0, mu):
        fitness = []
        xmin = self.permutation
        xnext = 0
        temp = t0
        fmin = self.computeCost()
        fitness.append(fmin)
        for k in range(100):
            neighbours = self.getNeighbours()
            # print(neighbours)
            for l in range(1, 100):
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
