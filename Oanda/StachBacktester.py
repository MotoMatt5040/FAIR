import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import tpqoa
from datetime import date, timedelta, datetime
import keyboard
import pickle
import yfinance as yf

plt.style.use('seaborn')

# df = pd.read_csv('Materials/forex_pairs.csv', parse_dates=['Date'], index_col='Date')
api = tpqoa.tpqoa('oanda.cfg')


class StachBacktester:
    """ Class for the vectorized backtesting of SMA-based trading strategies.
    """

    def __init__(self, instrument, start, end, granularity, price, k_period,
                 d_period):  # ticker: str, SMA_S: int, SMA_L: int, start: str, end: str):
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
        self.price = price
        self.granularity = granularity
        self.start = start
        self.end = end
        self.results = None

        self.k_period = k_period
        self.d_period = d_period

        self.get_data()
        self.prepare_data()

    def __repr__(self):
        return f'SMABacktester(ticker = {self._instrument}, start = {self.start}, end = {self.end})'

    def get_data(self):
        """ Imports the data from forex_pairs.csv (source can be changed).
        """
        # print(api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price))
        raw = api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity,
                              price=self.price)
        # print(raw.head(10).to_string())
        # raw = raw.c.to_frame().dropna()
        raw = raw.loc[self.start: self.end].copy()
        raw.rename(columns={'c': 'close'}, inplace=True)
        raw.rename(columns={'h': 'high'}, inplace=True)
        raw.rename(columns={'l': 'low'}, inplace=True)
        raw['returns'] = np.log(raw.close / raw.close.shift(1))
        self.data = raw
        # print(raw)
        print(raw.head(10).to_string())
        return raw

    def prepare_data(self):
        """Prepares the data for strategy backtesting (strategy-specific).
        """
        data = self.data.copy()

        self.data = data

    def set_parameters(self, k_period=None, d_period=None):
        """ Updates SMA parameters and the prepared dataset.
        """

    def test_strategy(self):
        """ Backtests the SMA-based trading strategy.
        """
        data = self.data.copy().dropna()
        # Define periods
        # k_period = 14
        # d_period = 3
        # Adds a "n_high" column with max value of previous 14 periods
        data['n_high'] = data['high'].rolling(self.k_period).max()
        # Adds an "n_low" column with min value of previous 14 periods
        data['n_low'] = data['low'].rolling(self.k_period).min()
        # Uses the min/max values to calculate the %k (as a percentage)
        data['k'] = (data['close'] - data['n_low']) * 100 / (data['n_high'] - data['n_low'])
        # Uses the %k to calculates a SMA over the past 3 values of %k
        data['d'] = data['k'].rolling(self.d_period).mean()

        data.ta.stoch(high='high', low='low', k=self.k_period, d=self.d_period, append=True)
        data.dropna(inplace=True)
        # print(data.head(10).to_string())

        # Overbought status
        # if k > 80 and d > 80 and k < d:
        #     sell
        data['position'] = np.where((data['k'] > 80.0) & (data['d'] > 80.0) & (data['k'] < data['d']), -1, np.nan)
        # Oversold status
        # else if k < 20 and d < 20 and k > d:
        data['position'] = np.where((data['k'] < 20.0) & (data['d'] < 20.0) & (data['k'] > data['d']), 1, np.nan)
        data["position"] = data.position.ffill().fillna(0)
        data['strategy'] = data['position'].shift(1) * data['returns']


        data.dropna(inplace=True)

        # print(data)
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
            title = f'{self._instrument} | k = {self.k_period} | d = {self.d_period}'
            self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(12, 8))
            plt.show()

    def optimize_parameters(self, k_period, d_period):
        """ Finds the optimal strategy (global maximum) given the SMA parameter ranges.

                Parameters
                ----------
                SMA_S_range, SMA_L_range: tuple
                    tuples of the form (start, end, step size)
        """
        combinations = list(product(range(*k_period), range(*d_period)))
        print(f'{len(combinations)} strategies being tested')

        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters(comb[0], comb[1])
            results.append(self.test_strategy()[0])
        print(self.results.head(10).to_string())

        best_perf = np.max(results)  # best performance
        opt = combinations[np.argmax(results)]  # optimal parameters

        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1])
        self.test_strategy()

        # create a df with many results
        many_results = pd.DataFrame(data=combinations, columns=['k_period', 'd_period'])
        many_results['performance'] = results
        self.results_overview = many_results

        pickle.dump(opt, open("stach_update.pkl", "wb"))

        return opt, best_perf


if __name__ == '__main__':
    tester = StachBacktester(instrument='EUR_USD', start=str(datetime.now() - timedelta(days=19))[:-7],
                           end=str(datetime.now())[:-7], granularity='M5', price='B', k_period=14, d_period=3)

    print(tester.test_strategy())
    tester.plot_results()

    print(tester.optimize_parameters(k_period=(1, 50, 1), d_period=(1, 50, 1)))

    tester.plot_results()

    wait = True
    while wait:
        if keyboard.is_pressed('1'):
            wait = False
    # tester.plot_results()
