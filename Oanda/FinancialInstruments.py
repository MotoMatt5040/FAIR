from typing import Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use('seaborn')

# class FinancialInstrument():
#     """Class for analyzing Financial Instruments like stocks.
#
#     Attributes
#     ==========
#     ticker: str
#         _ticker symbol with which to work with
#     start: str
#         start date for data retrieval
#     end: str
#         end date for data retrieval
#
#     Methods
#     =======
#     get_data:
#         returns finance data
#     log_returns:
#         crates a log returns category in self.data
#     plot_prices:
#         plots prices
#     plot_return:
#         plots returns
#     set_ticker:
#         sets new ticker
#     mean_return:
#         resamples mean returns at specified frequency
#     std_return:
#         resamples standard return at specified frequency
#     annualised_perf:
#         resamples annualised performance
#
#     """
#
#     def __init__(self, ticker: Union[list[str], str], start: str, end: str):
#         self._ticker = ticker
#         self.start = start
#         self.end = end
#         self.get_data()
#         self.log_returns()
#
#     def __repr__(self):
#         return "FinancialInstrument(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)
#
#     def get_data(self):
#         raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
#         raw.rename(columns={'Close': 'price'}, inplace=True)
#         self.data = raw
#         return raw
#
#     def log_returns(self):
#         self.data['log_returns'] = np.log(self.data.price / self.data.price.shift(1))
#
#     def plot_prices(self):
#         self.data.price.plot(figsize=(12, 8))
#         plt.title(f'Price Chart: {self._ticker}', fontsize=15)
#         plt.show()
#
#     def plot_return(self, kind: str = 'ts'):
#         if kind == 'ts':
#             self.data.log_returns.plot(figsize=(12, 8))
#             plt.title(f'Returns: {self._ticker}', fontsize=15)
#             plt.show()
#         elif kind == 'hist':
#             self.data.log_returns.hist(figsize=(12, 8), bins=int(np.sqrt(len(self.data))))
#             plt.title(f'Frequency of Returns: {self._ticker}', fontsize=15)
#             plt.show()
#
#     def set_ticker(self, ticker=None):
#         if ticker is not None:
#             self._ticker = ticker
#         self.get_data()
#         self.log_returns()
#
#     def mean_return(self, freq=None):
#         if freq is None:
#             return self.data.log_returns.mean()
#         else:
#             resampled_price = self.data.price.resample(freq).last()
#             resampled_returns = np.log(resampled_price / resampled_price.shift(1))
#             return resampled_returns.mean()
#
#     def std_returns(self, freq=None):
#         if freq is None:
#             return self.data.log_returns.std()
#         else:
#             resampled_price = self.data.price.resample(freq).last()
#             resampled_returns = np.log(resampled_price / resampled_price.shift(1))
#             return resampled_returns.std()
#
#     def annualised_perf(self):
#         mean_return = round(self.data.log_returns.mean() * 252, 3)
#         risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
#         print(f'Return: {mean_return} | Risk: {risk}')


class FinancialInstrumentBase():

    def __init__(self, ticker: Union[list[str], str], start: str, end: str):
        self._ticker = ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()

    def __repr__(self):
        return "FinancialInstrumentBase(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

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


class RiskReturn():

    def __init__(self, ticker: Union[list[str], str], start: str, end: str):
        self._ticker = ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()

    def __repr__(self):
        return "RiskReturn(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

    def mean_return(self, freq=None):
        if freq is None:
            return self.data.log_returns.mean()
        else:
            resampled_price = self.data.price.resample(freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.mean()

    def std_returns(self, freq=None):
        if freq is None:
            return self.data.log_returns.std()
        else:
            resampled_price = self.data.price.resample(freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.std()

    def annualised_perf(self):
        mean_return = round(self.data.log_returns.mean() * 252, 3)
        risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
        print(f'Return: {mean_return} | Risk: {risk}')

stock = RiskReturn('AAPL', '2015-01-01', '2019-12-31')
print(stock)

# stock.set_ticker('GE')

# print(stock._ticker)
# print(stock.data)
# stock.data.log_returns.plot()
# plt.show()
# stock.data.log_returns.hist(bins=100)
# plt.show()
stock.plot_prices()
stock.plot_return()

print(stock.mean_return())
print(stock.mean_return('m'))
print(stock.std_returns())
print(stock.std_returns('m'))
stock.annualised_perf()
