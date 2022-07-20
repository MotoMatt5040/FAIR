import MetaTrader5 as mt5
import pytz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import tpqoa
from datetime import date, timedelta, datetime
import keyboard
import pickle
plt.style.use('seaborn')

# df = pd.read_csv('Materials/forex_pairs.csv', parse_dates=['Date'], index_col='Date')
api = tpqoa.tpqoa('oanda.cfg')

class MACDRSIBacktester:

    """ Class for the vectorized backtesting of SMA-based trading strategies.
    """


    def __init__(self, instrument, start: datetime, end: datetime, MSMA: int, SMA_L: int, granularity, price):  # ticker: str, SMA_S: int, SMA_L: int, start: str, end: str):
        """
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        MSMA: int
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
        self.MSMA = MSMA
        self.SMA_L = SMA_L
        self.price = price
        self.granularity = granularity
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        self.prepare_data()

    def __repr__(self):
        return f'SMABacktester(ticker = {self._instrument}, SMA = {self.MSMA}, SMA_L = {self.SMA_L}, start = {self.start}, end = {self.end})'

    def get_data(self):
        """ Imports the data from forex_pairs.csv (source can be changed).
        """
        # print(api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price))
        # raw = api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price)
        # get bars from USDZAR H1 within the interval of 2020.01.01 00:00 - 2020.05.05 in UTC time zone

        raw = mt5.copy_rates_range(self._instrument,  self.granularity, self.start, self.start, self.end)
        raw = raw.loc[self.start: self.end].copy()
        # raw.rename(columns={'close': 'price'}, inplace=True)
        raw['returns'] = np.log(raw.close / raw.close.shift(1))
        self.data = raw
        return raw

    def prepare_data(self):
        """Prepares the data for strategy backtesting (strategy-specific).
        """
        data = self.data.copy()
        data['SMA'] = data['close'].rolling(self.MSMA).mean()
        data['SMA_L'] = data['close'].rolling(self._SMA_L).mean()
        self.data = data

    def set_parameters(self, SMA_S = None, SMA_L = None):
        """ Updates SMA parameters and the prepared dataset.
        """
        if SMA_S is not None:
            self._SMA_S = SMA_S
            self.data['SMA_S'] = self.data['close'].rolling(self.MSMA).mean()
        if SMA_L is not None:
            self._SMA_L = SMA_L
            self.data['SMA_L'] = self.data['close'].rolling(self.SMA_L).mean()

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
            title = f'{self._instrument} | {self.MSMA} | SMA | {self.SMA_L} | SMA_L'
            self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(12, 8))
            plt.show()

    def optimize_parameters(self, SMA_range, SMA_L_range):
        """ Finds the optimal strategy (global maximum) given the SMA parameter ranges.

                Parameters
                ----------
                SMA_S_range, SMA_L_range: tuple
                    tuples of the form (start, end, step size)
        """
        combinations = list(product(range(*SMA_range), range(*SMA_L_range)))
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
        many_results = pd.DataFrame(data=combinations, columns=['SMA', 'SMA_L'])
        many_results['performance'] = results
        self.results_overview = many_results

        pickle.dump(opt, open("macdrsi_update.pkl", "wb"))

        return opt, best_perf

if __name__ == '__main__':
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")

    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    start = datetime(2022, 7, 10, tzinfo=timezone)
    end = datetime(2022, 7, 13, tzinfo=timezone)

    tester = MACDRSIBacktester(instrument='EURUSD', start=start, end=end, granularity=mt5.TIMEFRAME_M5, price='B',
                               SMA=9, SMA_L=1)


    print(tester.test_strategy())
    # tester.plot_results()

    print(tester.optimize_parameters((1, 50, 1), (51, 170, 1))[0])

    wait = True
    while wait:
        if keyboard.is_pressed('1'):
            wait = False
    # tester.plot_results()


# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# import the 'pandas' module for displaying data obtained in the tabular form


pd.set_option('display.max_columns', 5000)  # number of columns to be displayed
pd.set_option('display.width', 15000)  # max table width to display

# import pytz module for working with time zone


# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()



# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# create DataFrame out of the obtained data
# UZH = pd.DataFrame(UCrateH)
# print(UZH)
