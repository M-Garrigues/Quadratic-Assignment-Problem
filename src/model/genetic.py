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

    def setParameters(self, population, selector, crossMultiple=False, crossProba=0.0, mutationProba= 0.01):
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
        scores  = [self._population.size]
        i = 0

        for permutation in self._population:
            scores[i] = permutation.computeCost()

        return scores

    def selectBest(self, scores):
        


