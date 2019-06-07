import copy
import math

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
            self._population[i] = copy.deepcopy(self._map.permutation)
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


data = Taixxa()
data.loadFile("../../notebooks/tai12a.dat")
algo = GeneticAlgorithm(data)
algo.setParameters(population=10, selector=1)
best = algo.selectBestCouples(algo.evaluatePopulation())
print(algo.evaluatePopulation())

for b in best:
    print(b[1])
    print(b[0])
    print("----")

print("--azfazfazfazffzafazazfzafzafzaf--")
