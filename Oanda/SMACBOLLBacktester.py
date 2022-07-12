import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import tpqoa
from datetime import date, timedelta
import keyboard
import pickle
plt.style.use('seaborn')

# df = pd.read_csv('Materials/forex_pairs.csv', parse_dates=['Date'], index_col='Date')
api = tpqoa.tpqoa('oanda.cfg')

class SMACBOLLBacktester:

    """ Class for the vectorized backtesting of SMA-based trading strategies.
    """


    def __init__(self, instrument, start, end, SMA_S: int, SMA_L: int, granularity, price, SMA, dev, tc):  # ticker: str, SMA_S: int, SMA_L: int, start: str, end: str):
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
        self.SMA = SMA
        self.dev = dev
        self.tc = tc

        self.get_data()
        self.prepare_data()


    def __repr__(self):
        return f'SMABacktester(ticker = {self._instrument}, SMA_S = {self._SMA_S}, SMA_L = {self._SMA_L}, start = {self.start}, end = {self.end})'

    def get_data(self):
        """ Imports the data from forex_pairs.csv (source can be changed).
        """
        # print(api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price))
        raw = api.get_history(instrument=self._instrument, start=self.start, end=self.end, granularity=self.granularity, price=self.price)
        raw = raw.c.to_frame().dropna()
        raw = raw.loc[self.start: self.end].copy()
        raw.rename(columns={'c': 'price'}, inplace=True)
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw
        print(raw)
        return raw

    def prepare_data(self):
        """Prepares the data for strategy backtesting (strategy-specific).
        """
        data = self.data.copy()
        data['SMA_S'] = data['price'].rolling(self._SMA_S).mean()
        data['SMA_L'] = data['price'].rolling(self._SMA_L).mean()
        data["SMA"] = data["price"].rolling(self.SMA).mean()
        data["Lower"] = data["SMA"] - data["price"].rolling(self.SMA).std() * self.dev
        data["Upper"] = data["SMA"] + data["price"].rolling(self.SMA).std() * self.dev
        self.data = data

    def set_parameters(self, SMA_S = None, SMA_L = None, SMA = None, dev = None):
        """ Updates SMA parameters and the prepared dataset.
        """
        if SMA_S is not None:
            self._SMA_S = SMA_S
            self.data['SMA_S'] = self.data['price'].rolling(self._SMA_S).mean()
        if SMA_L is not None:
            self._SMA_L = SMA_L
            self.data['SMA_L'] = self.data['price'].rolling(self._SMA_L).mean()
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
        """ Backtests the SMA-based trading strategy.
        """
        data = self.data.copy().dropna()
        data['sposition'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        data['strategy'] = data['sposition'].shift(1) * data['returns']

        data["distance"] = data.price - data.SMA
        data["bposition"] = np.where(data.price <= data.Lower, 1, np.nan)
        data["bposition"] = np.where(data.price >= data.Upper, -1, data["bposition"])
        data["bposition"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["bposition"])
        data["bposition"] = data.bposition.ffill().fillna(0)
        data["strategy"] = data.bposition.shift(1) * data["returns"]
        data.dropna(inplace=True)

        # data['sposition'] = np.where(data.)

        # print(data.head(10).to_string())

        # Define position
        data['position'] = np.where(data['sposition'] == data['bposition'], data['sposition'], data['bposition'])

        # determine the number of trades in each bar
        data["trades"] = data.position.diff().fillna(0).abs()

        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * self.tc


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
            title = f'{self._instrument} | {self._SMA_S} | SMA_S | {self._SMA_L} | SMA_L | SMA = {self.SMA } | ' \
                    f'dev = {self.dev} | TC = {self.tc}'
            self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(12, 8))
            plt.show()

    def optimize_parameters(self, SMA_S_range, SMA_L_range, SMA_range, dev_range):
        """ Finds the optimal strategy (global maximum) given the SMA parameter ranges.

                Parameters
                ----------
                SMA_S_range, SMA_L_range: tuple
                    tuples of the form (start, end, step size)
        """
        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range), range(*SMA_range), range(*dev_range)))
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
        many_results = pd.DataFrame(data=combinations, columns=['SMA_S', 'SMA_L', 'SMA', 'dev'])
        many_results['performance'] = results
        self.results_overview = many_results

        pickle.dump(opt, open("sma_update.pkl", "wb"))

        return opt, best_perf

if __name__ == '__main__':
    tester = SMACBOLLBacktester(instrument='EUR_USD', start=str(date.today() - timedelta(30)), end=str(date.today()),
                                granularity='M15', price='B', SMA_S=9, SMA_L=1, SMA=20, dev=2, tc=0.0)

    print(tester.test_strategy())
    tester.plot_results()

    print(tester.optimize_parameters(SMA_S_range=(1, 20, 1), SMA_L_range=(21, 170, 1),
                                     SMA_range=(10, 50, 1), dev_range=(1, 3, 1))[0])

    tester.plot_results()

    wait = True
    while wait:
        if keyboard.is_pressed('1'):
            wait = False
    # tester.plot_results()

