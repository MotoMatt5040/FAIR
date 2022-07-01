import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import tpqoa
plt.style.use('seaborn')

# df = pd.read_csv('Materials/forex_pairs.csv', parse_dates=['Date'], index_col='Date')
api = tpqoa.tpqoa('oanda.cfg')

class SMABacktester:

    """ Class for the vectorized backtesting of SMA-based trading strategies.
    """


    def __init__(self, instrument, start, end, SMA_S: int, SMA_L: int, granularity, price):  # ticker: str, SMA_S: int, SMA_L: int, start: str, end: str):
        """
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        SMA_S: int
            moving window in bars (e.g. days) for shorter SMA
        SMA_L: int
            moving window in bars (e.g. days) for longer SMA
        start: str
            start date for data import
        end: str
            end date for data import
        """

        # self.ticker = ticker
        self._instrument = instrument
        self._SMA_S = SMA_S
        self._SMA_L = SMA_L
        self.price = price
        self.granularity = granularity
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        self.prepare_data()

    def __repr__(self):
        return f'SMABacktester(ticker = {self._instrument}, SMA_S = {self._SMA_S}, SMA_L = {self._SMA_L}, start = {self.start}, end = {self.end})'

    def get_data(self):
        """ Imports the data from forex_pairs.csv (source can be changed).
        """
        print(api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price))
        raw = api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price)
        raw = raw.c.to_frame().dropna()
        raw = raw.loc[self.start: self.end].copy()
        raw.rename(columns={'c': 'price'}, inplace=True)
        # print(raw)
        # print(raw)
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw
        return raw

    # def get_data(self):
    #     """ Imports the data from forex_pairs.csv (source can be changed).
    #     """
    #     raw = pd.read_csv('Materials/forex_pairs.csv', parse_dates=['Date'], index_col='Date')
    #     raw = raw[self.ticker].to_frame().dropna()
    #     raw = raw.loc[self.start: self.end].copy()
    #     raw.rename(columns={self.ticker: 'price'}, inplace=True)
    #     raw['returns'] = np.log(raw / raw.shift(1))
    #     self.data = raw
    #     return raw

    def prepare_data(self):
        """Prepares the data for strategy backtesting (strategy-specific).
        """
        data = self.data.copy()
        data['SMA_S'] = data['price'].rolling(self._SMA_S).mean()
        data['SMA_L'] = data['price'].rolling(self._SMA_L).mean()
        self.data = data


    def set_parameters(self, SMA_S = None, SMA_L = None):
        """ Updates SMA parameters and the prepared dataset.
        """
        if SMA_S is not None:
            self._SMA_S = SMA_S
            self.data['SMA_S'] = self.data['price'].rolling(self._SMA_S).mean()
        if SMA_L is not None:
            self._SMA_L = SMA_L
            self.data['SMA_L'] = self.data['price'].rolling(self._SMA_L).mean()

    def test_strategy(self):
        """ Backtests the SMA-based trading strategy.
        """
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['returns']
        data.dropna(inplace=True)
        data['creturns'] = data['returns'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data

        perf = data['cstrategy'].iloc[-1]
        outperf = perf - data['creturns'].iloc[-1]
        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        """ Plots the performance of the trading strategy and compares to "buy and hold".
        """
        if self.results is None:
            print('Run test_strategy() strategy first.')
        else:
            title = f'{self._instrument} | {self._SMA_S} | SMA_S | {self._SMA_L} | SMA_L'
            self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(12, 8))

    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        """ Finds the optimal strategy (global maximum) given the SMA parameter ranges.

                Parameters
                ----------
                SMA_S_range, SMA_L_range: tuple
                    tuples of the form (start, end, step size)
        """
        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range)))
        print(f'{len(combinations)} strategies being tested')

        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters(comb[0], comb[1])
            results.append(self.test_strategy()[0])

        best_perf = np.max(results)  # best performance
        opt = combinations[np.argmax(results)]  # optimal parameters

        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1])
        self.test_strategy()

        # create a df with many results
        many_results = pd.DataFrame(data=combinations, columns=['SMA_S', 'SMA_L'])
        many_results['performance'] = results
        self.results_overview = many_results

        return opt, best_perf
