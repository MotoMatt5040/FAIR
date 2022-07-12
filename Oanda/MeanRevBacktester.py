import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from datetime import date, timedelta, datetime
import tpqoa

plt.style.use("seaborn")
api = tpqoa.tpqoa('oanda.cfg')


class MeanRevBacktester():
    ''' Class for the vectorized backtesting of Bollinger Bands-based trading strategies.
    '''

    def __init__(self, instrument, start, end, granularity, price, SMA, dev, tc):
        '''
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        SMA: int
            moving window in bars (e.g. days) for SMA
        dev: int
            distance for Lower/Upper Bands in Standard Deviation units
        start: str
            start date for data import
        end: str
            end date for data import
        tc: float
            proportional transaction/trading costs per trade
        '''
        # self.ticker = ticker
        self._instrument = instrument
        self.price = price
        self.granularity = granularity
        self.start = start
        self.end = end
        self.results = None
        self.SMA = SMA
        self.dev = dev
        self.tc = tc

        self.get_data()
        self.prepare_data()

    def __repr__(self):
        rep = "MeanRevBacktester(symbol = {}, SMA = {}, dev = {}, start = {}, end = {})"
        return rep.format(self._instrument, self.SMA, self.dev, self.start, self.end)

    def get_data(self):
        ''' Imports the data from intraday_pairs.csv (source can be changed).
        '''
        # raw = pd.read_csv("../Testing/Oanda/Materials/intraday_pairs.csv", parse_dates=["time"], index_col="time")
        raw = api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity,
                              price=self.price)
        raw = raw.c.to_frame().dropna()
        raw = raw.loc[self.start: self.end].copy()
        raw.rename(columns={'c': 'price'}, inplace=True)
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw
        print(raw)
        return raw

    def prepare_data(self):
        '''Prepares the data for strategy backtesting (strategy-specific).
        '''
        data = self.data.copy()
        data["SMA"] = data["price"].rolling(self.SMA).mean()
        data["Lower"] = data["SMA"] - data["price"].rolling(self.SMA).std() * self.dev
        data["Upper"] = data["SMA"] + data["price"].rolling(self.SMA).std() * self.dev
        self.data = data.dropna()
        print(self.data)

    def set_parameters(self, SMA=None, dev=None):
        ''' Updates parameters (SMA, dev) and the prepared dataset.
        '''
        if SMA is not None:
            self.SMA = SMA
            self.data["SMA"] = self.data["price"].rolling(self.SMA).mean()
            self.data["Lower"] = self.data["SMA"] - self.data["price"].rolling(self.SMA).std() * self.dev
            self.data["Upper"] = self.data["SMA"] + self.data["price"].rolling(self.SMA).std() * self.dev

        if dev is not None:
            self.dev = dev
            self.data["Lower"] = self.data["SMA"] - self.data["price"].rolling(self.SMA).std() * self.dev
            self.data["Upper"] = self.data["SMA"] + self.data["price"].rolling(self.SMA).std() * self.dev

    def test_strategy(self):
        ''' Backtests the Bollinger Bands-based trading strategy.
        '''
        data = self.data.copy().dropna()
        data["distance"] = data.price - data.SMA
        data["position"] = np.where(data.price < data.Lower, 1, np.nan)
        data["position"] = np.where(data.price > data.Upper, -1, data["position"])
        data["position"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["position"])
        data["position"] = data.position.ffill().fillna(0)
        data["strategy"] = data.position.shift(1) * data["returns"]
        data.dropna(inplace=True)

        # determine the number of trades in each bar
        data["trades"] = data.position.diff().fillna(0).abs()

        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * self.tc

        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data


        perf = data["cstrategy"].iloc[-1]  # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1]  # out-/underperformance of strategy

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        ''' Plots the performance of the trading strategy and compares to "buy and hold".
        '''
        if self.results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | SMA = {} | dev = {} | TC = {}".format(self._instrument, self.SMA, self.dev, self.tc)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))
            plt.show()

    def optimize_parameters(self, SMA_range, dev_range):
        ''' Finds the optimal strategy (global maximum) given the Bollinger Bands parameter ranges.

        Parameters
        ----------
        SMA_range, dev_range: tuple
            tuples of the form (start, end, step size)
        '''

        combinations = list(product(range(*SMA_range), range(*dev_range)))
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
        many_results = pd.DataFrame(data=combinations, columns=["SMA", "dev"])
        many_results["performance"] = results
        self.results_overview = many_results

        return opt, best_perf


# mr = MeanRevBacktester('EURUSD', 30, 2, '2018-01-01', '2019-12-30', 0.000, 100000.0)

mr = MeanRevBacktester(instrument='EUR_USD', start=str(datetime.now() - timedelta(days=30))[:-7], end=str(datetime.now())[:-7],
                                granularity='H1', price='B', SMA=30, dev=1, tc=0.0)

print(mr.test_strategy())
mr.plot_results()

print(mr.optimize_parameters((5, 70, 1), (1, 3, 1)))
mr.plot_results()
