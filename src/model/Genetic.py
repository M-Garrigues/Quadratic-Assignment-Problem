import copy
import random
import numpy as np

import math

from Permutation import Permutation
from Taixxa import Taixxa
from FitnessViewer import FitnessViewer


class GeneticAlgorithm:

    def __init__(self, taixxa):
        self._bestPermutation = None
        self._bestFitness = math.inf
        self._selector = None
        self._map = taixxa
        self._crossMultiple = False
        self._crossProbability = 0.0
        self._mutationProbability = 0.0

        self._population = None
        self._fitness = None

    def setParameters(self, population, selector, crossMultiple=False, crossProba=0.0, mutationProba=0.01):
        self._population = [None] * population
        self._crossMultiple = crossMultiple
        self._crossProbability = crossProba
        self._mutationProbability = mutationProba
        self.initialise()
        self._bestPermutation = None
        self._bestFitness = math.inf

    def initialise(self):

        for i in range(len(self._population)):
            self._population[i] = copy.deepcopy(self._map._perm)
            self._population[i].shuffle()

        self._bestPermutation = None
        self._fitness = list()

    def iterate(self, nbIterations):

        self.initialise()

        for i in range(nbIterations):

            #print(self._population[0][:])
            #print(len(self._population))
            scores = self.evaluatePopulation()
            couples = self.selectBestCouples(scores)
            self.crossover(couples)
            self.mutate()
            #print(self._bestPermutation.computeCost(self._map))
            #(self._bestFitness)

        return self._bestFitness, self._fitness, self._bestPermutation

    def evaluatePopulation(self):

        scores = list()

        for permutation in self._population:
            scores.append(permutation.computeCost(self._map))

        return scores

    def selectBestCouples(self, scores):

        selected = list()

        for i in range(int(len(self._population) / 2.5)):
            indexMin = scores.index(min(scores))

            if i is 0:
                self._fitness.append(scores[indexMin])
            if i is 0 and self._bestFitness > scores[indexMin]:

                self._bestFitness = scores[indexMin]
                self._bestPermutation = copy.deepcopy(self._population[indexMin])

            scores[indexMin] = math.inf

            selected.append((self._population[indexMin], i))

        couplesIndex = list()
        for coupleA in selected:
            for coupleB in selected:
                if coupleA[1] < coupleB[1]:
                    couplesIndex.append(
                        (coupleA[0].computeCost(self._map) + coupleB[0].computeCost(self._map), (coupleA, coupleB)))
        couplesIndex.sort(key=lambda x: x[0])
        ret = list()
        for e in [sl[1] for sl in couplesIndex[:int(len(self._population) / 2)]]:
            ret.append((e[0][0], e[1][0]))


        return ret

    def crossover(self, couples):

        newGeneration = list()

        for couple in couples:

            nbPerm = 1
            if self._crossMultiple:
                nbPerm = int(self._crossProbability * len(self._population[0]._perm) + 1)

            permA = self.pickGenes(main=couple[0], second=couple[1], nbPermutations=nbPerm)
            permB = self.pickGenes(main=couple[1], second=couple[0], nbPermutations=nbPerm)

            newGeneration.append(permA)
            newGeneration.append(permB)

        self._population = newGeneration

    def pickGenes(self, main, second, nbPermutations):

        size = len(main._perm)
        childGenes = [None] * size
        permCrossed = list()

        indexes = random.sample(range(0, size - 1), nbPermutations)
        for i in indexes:
            childGenes[i] = second[i]
            permCrossed.append((childGenes[i], main[i]))

        for i in range(size):
            if childGenes[i] is None:
                if main[i] in [e[0] for e in permCrossed]:
                    for tup in permCrossed:
                        if main[i] == tup[0] and tup[1] not in childGenes:
                            childGenes[i] = tup[1]
                else:
                    childGenes[i] = main[i]

        left = self.find_missing(childGenes, len(childGenes))
        for gene in childGenes:
            if gene is None:
                childGenes[childGenes.index(gene)] = left[0]
                left.pop(0)
        return Permutation(size, childGenes)

    def mutate(self):

        for permutation in self._population:

            if random.uniform(0, 1) < self._mutationProbability:
                i, j = random.sample(range(0, len(permutation[:]) - 1), 2)
                permutation.permute(i, j)

    def find_missing(self, lst, size):
        return [x for x in range(size)
                if x not in lst]

