from typing import Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use('seaborn')


class FinancialInstrumentBase:

    """Class for analyzing Financial Instruments like Stocks/Forex Pairs.

    Attributes
    ==========
    ticker: str
        _ticker symbol with which to work with
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Methods
    =======
    get_data:
        Retrieves daily price data (from yahoo finance) and prepares the data
    log_returns:
        Calculates log returns
    plot_prices:
        Creates a price chart
    plot_return:
        Plots log returns either as time series ("ts") or histogram ("hist")
    set_ticker:
        sets a new ticker
    mean_return:
        Calculates mean return
    std_return:
        Calculates the standard deviation of returns (risk)
    annualised_perf:
        Calculates annualised return and risk
    """

    def __init__(self, ticker: Union[list[str], str], start: str, end: str):
        self._ticker = ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()

    def __repr__(self):
        return "FinancialInstrumentBase(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

    def get_data(self):
        """Retrieves daily price data (from yahoo finance) and prepares the data
        """
        raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
        raw.rename(columns={'Close': 'price'}, inplace=True)
        self.data = raw
        return raw

    def log_returns(self):
        """Calculates log returns
        """
        self.data['log_returns'] = np.log(self.data.price / self.data.price.shift(1))

    def plot_prices(self):
        """Creates a price chart
        """
        self.data.price.plot(figsize=(12, 8))
        plt.title(f'Price Chart: {self._ticker}', fontsize=15)
        plt.show()

    def plot_return(self, kind: str = 'ts'):
        """Plots log returns either as time series ("ts") or as histogram ("hist")
        """
        if kind == 'ts':
            self.data.log_returns.plot(figsize=(12, 8))
            plt.title(f'Returns: {self._ticker}', fontsize=15)
            plt.show()
        elif kind == 'hist':
            self.data.log_returns.hist(figsize=(12, 8), bins=int(np.sqrt(len(self.data))))
            plt.title(f'Frequency of Returns: {self._ticker}', fontsize=15)
            plt.show()

    def set_ticker(self, ticker=None):
        """sets a new ticker
        """
        if ticker is not None:
            self._ticker = ticker
        self.get_data()
        self.log_returns()


class RiskReturn(FinancialInstrumentBase):

    def __init__(self, ticker, start, end, freq=None):
        self.freq = freq
        super().__init__(ticker, start, end)

    def __repr__(self):
        return "RiskReturn(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

    def mean_return(self):
        """Calculates mean return
        """
        if self.freq is None:
            return self.data.log_returns.mean()
        else:
            resampled_price = self.data.price.resample(self.freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.mean()

    def std_returns(self):
        """Calculates the standard deviation of returns (risk)
        """
        if self.freq is None:
            return self.data.log_returns.std()
        else:
            resampled_price = self.data.price.resample(self.freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.std()

    def annualised_perf(self):
        """Calculates annualised return and risk
        """
        mean_return = round(self.data.log_returns.mean() * 252, 3)
        risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
        print(f'Return: {mean_return} | Risk: {risk}')

# stock = RiskReturn('AAPL', '2015-01-01', '2019-12-31', freq='w')
# # print(stock)
#
# # stock.set_ticker('GE')
#
# # print(stock._ticker)
# # print(stock.data)
# # stock.data.log_returns.plot()
# # stock.data.log_returns.hist(bins=100)
# # stock.plot_prices()
# # stock.plot_return()
#
# print(stock.mean_return())
# print(stock.mean_return())
# print(stock.std_returns())
# print(stock.std_returns())
# stock.annualised_perf()
#
# # print(stock.freq)
