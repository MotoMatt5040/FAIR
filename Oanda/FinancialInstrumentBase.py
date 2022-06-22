from typing import Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use('seaborn')

class FinancialInstrumentBase():
    def __init__(self, ticker: Union[list[str], str], start: str, end: str):
        self._ticker = ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()

    def __repr__(self):
        return "FinancialInstrument(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

    def get_data(self):
        raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
        raw.rename(columns={'Close': 'price'}, inplace=True)
        self.data = raw
        return raw

    def log_returns(self):
        self.data['log_returns'] = np.log(self.data.price / self.data.price.shift(1))

    def plot_prices(self):
        self.data.price.plot(figsize=(12, 8))
        plt.title(f'Price Chart: {self._ticker}', fontsize=15)
        plt.show()

    def plot_return(self, kind: str = 'ts'):
        if kind == 'ts':
            self.data.log_returns.plot(figsize=(12, 8))
            plt.title(f'Returns: {self._ticker}', fontsize=15)
            plt.show()
        elif kind == 'hist':
            self.data.log_returns.hist(figsize=(12, 8), bins=int(np.sqrt(len(self.data))))
            plt.title(f'Frequency of Returns: {self._ticker}', fontsize=15)
            plt.show()

    def set_ticker(self, ticker=None):
        if ticker is not None:
            self._ticker = ticker
        self.get_data()
        self.log_returns()
