import pandas as pd
import numpy as np
import tpqoa
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
import pickle

plt.style.use('seaborn')
api = tpqoa.tpqoa('oanda.cfg')

class Peaks:
    ''' Class for the vectorized backtesting of peaks().
    '''

    def __init__(self, symbol, start, end, granularity='M1'):
        '''
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        start: str
            start date for data import
        end: str
            end date for data import
        '''
        self.symbol = symbol
        self.start = start
        self.end = end
        self.granularity = granularity
        self.results = None
        self.get_data()

    def __repr__(self):
        rep = "Peaks(symbol = {}, start = {}, end = {})"
        return rep.format(self.symbol, self.start, self.end)

    def get_data(self):
        ''' Imports the data from five_minute_pairs.csv (source can be changed).
        '''
        # raw = pd.read_csv("../Testing/Oanda/Materials/five_minute_pairs.csv", parse_dates=["time"], index_col="time")
        raw = api.get_history(instrument=self.symbol, start=self.start, end=self.end,
                              granularity=self.granularity, price="B")
        # print(raw.to_string())
        # raw = raw[self.symbol].to_frame().dropna()
        raw = raw.loc[self.start:self.end]
        # raw.rename(columns={self.symbol: "price"}, inplace=True)
        # raw["returns"] = np.log(raw.c / raw.c.shift(1))
        self.data = raw
        print(raw)


    def peaks(self):
        '''
        :returns upper and lower price peaks
        '''

        return self.data.h.max(), self.data.l.min()

    def plot_results(self):
        ''' Plots the performance of the trading strategy and compares to "buy and hold".
        '''

        title = f"Peaks: {self.symbol}"
        self.data[["c"]].plot(title=title, figsize=(12, 8))
        plt.show()

p = Peaks(symbol='EUR_USD', start=str(datetime.now() - timedelta(days=3))[:-7], end=str(datetime.now())[:-7], granularity='M15')

print(p.peaks())
p.plot_results()