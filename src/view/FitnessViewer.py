import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FitnessViewer:

    def __init__(self, values):
        self._length = values.size
        self._values = pd.Series(values, index=pd.RangeIndex(stop=self._length))

    def plot(self,title):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(title)
        ax.plot(self._values)
        plt.show()

    def add(self, value):
        print(pd.Series(value))
        self._values.append(pd.Series(value), ignore_index=True)
        print(self._values)
        self._length += 1


