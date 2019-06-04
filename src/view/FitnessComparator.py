import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FitnessComparator:

    def __init__(self, df):
        self._length = df.size
        self._values = df

    def plot(self):
        self._values.cumsum()
        plt.figure()
        self._values.plot()
        plt.legend(loc='best')
        plt.show()

    def add(self, value):
        print(pd.Series(value))
        self._values.append(pd.Series(value), ignore_index=True)
        print(self._values)
        self._length += 1


fit = FitnessComparator(df=pd.DataFrame(np.random.randn(1000, 4), index=pd.RangeIndex(stop=1000), columns=list('ABCD')))
fit.plot()
