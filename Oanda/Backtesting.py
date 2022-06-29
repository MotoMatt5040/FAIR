import pandas as pd
import numpy as np


class Backtesting:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def __repr__(self):
        return 'Backtesting'

    def update_df(self, df: pd.DataFrame):
        self._df = df

    def returns(self):
        self._df['returns'] = np.log(self._df.price.div(self._df.price.shift(1)))

    def strategy(self):
        self._df = self._df.position.shift(1) * self._df['returns']

