class Permutation:

    def __init__(self, modulesNumber):
        self._perm = list(range(modulesNumber))

    def __getitem__(self, item):
        return self._perm[item]

    def permute(self, i, j):
        assert (i < self._perm.count, j < self._perm.count)
        tmp = self._perm[i]
        self._perm[i] = self._perm[j]
        self._perm[j] = tmp

    def get(self, i):
        return self._perm[i]

    def set(self, i, val):
        self._perm[i] = val
