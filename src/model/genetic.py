import copy
import random

import math

from src.model.Permutation import Permutation
from src.model.Taixxa import Taixxa


class GeneticAlgorithm:

    def __init__(self, taixxa):
        self._selector = None
        self._map = taixxa
        self._crossMultiple = False
        self._crossProbability = 0.0
        self._mutationProbability = 0.0

        self._population = None
        self._fitness = None
        self._best = None

    def setParameters(self, population, selector, crossMultiple=False, crossProba=0.0, mutationProba=0.01):
        self._population = [None] * population
        self._crossMultiple = crossMultiple
        self._crossProbability = crossProba
        self._mutationProbability = mutationProba
        self.initialise()

    def initialise(self):

        for i in range(len(self._population)):
            self._population[i] = copy.deepcopy(self._map._perm)
            self._population[i].shuffle()

        self._best = math.inf
        self._fitness = list()

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
                self._best = copy.deepcopy(self._population[indexMin])

            scores[indexMin] = math.inf

            selected.append((self._population[indexMin], i))

        couplesIndex = list()
        for coupleA in selected:
            for coupleB in selected:
                if coupleA[1] < coupleB[1]:
                    couplesIndex.append(
                        (coupleA[0].computeCost(self._map) + coupleB[0].computeCost(self._map), (coupleA, coupleB)))

        bestCouples = sorted(couplesIndex)[:int(len(self._population) / 2)]

        ret = list()
        for e in [sl[1] for sl in bestCouples]:
            ret.append((e[0][0], e[1][0]))

        return ret

    def crossover(self, couples):

        newGeneration = list()

        for couple in couples:

            nbPerm = 1
            if self._crossMultiple:
                nbPerm = self._crossProbability * len(self._population) + 1

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
                if not (main[i] in [e[0] for e in permCrossed]):
                    childGenes[i] = main[i]
                else:
                    childGenes[i] = permCrossed[0][1]
                    permCrossed.pop(0)

        return Permutation(size, childGenes)

    def mutate(self):

        for permutation in self._population:


            if random.uniform(0, 1) < self._mutationProbability:
                i, j = random.sample(range(0, len(permutation[:]) - 1), 2)
                permutation.permute(i, j)



data = Taixxa()
data.loadFile("../../notebooks/tai12a.dat")
algo = GeneticAlgorithm(data)
algo.setParameters(population=10, selector=1, mutationProba=0.2)
best = algo.selectBestCouples(algo.evaluatePopulation())
print(algo.evaluatePopulation())

for b in best:
    print(b[1])
    print(b[0])
    print("----")

print("--azfazfazfazffzafazazfzafzafzaf--")

algo.crossover(best)
algo.mutate()
