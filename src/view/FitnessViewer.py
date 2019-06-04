import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FitnessViewer:

    def __init__(self, length, values):
        self._length = length
        self._values = pd.Series(values, index=pd.RangeIndex(stop=self._length))

    def plot(self):
        #print(self._values)
        ts = self._values
        #ts = ts.cumsum()
        ts.plot()

        plt.show()

    def add(self, value):
        print(pd.Series(value))
        self._values.append(pd.Series(value), ignore_index=True)
        print(self._values)
        self._length += 1


viewer = FitnessViewer(10, np.random.randn(10))
viewer.plot()

viewer.add(5)
viewer.plot()
