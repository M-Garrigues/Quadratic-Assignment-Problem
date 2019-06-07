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
        self._population = [population]
        self._crossMultiple = crossMultiple
        self._crossProbability = crossProba
        self._mutationProbability = mutationProba
        self.initialise()

    def initialise(self):

        for i in range(self._population.size):
            self._population[i] = self._map.permutation.shuffle()

        self._best = 1000000000000000
        self._fitness = list()

    def evaluatePopulation(self):

        scores = list()

        for permutation in self._population:
            scores.append(permutation.computeCost())

        return scores

    def selectBest(self, scores):

        selected = list()

        for i in range(self._population.size / 2):
            indexMin = scores.index(min(scores))

            scores[indexMin] = 0

            selected.append((self._population[indexMin], i))

        return selected
