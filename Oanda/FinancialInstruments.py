import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use('seaborn')

class FinancialInstrument():
    """Class for analyzing Financial Instruments like stocks.

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
    get_date:

    """

    def __init__(self, ticker, start, end):
        self._ticker = ticker
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()

    def __repr__(self):
        return "FinancialInstrument(_ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)

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
        # plt.show()

    def plot_return(self, kind = 'ts'):
        if kind == 'ts':
            self.data.log_returns.plot(figsize=(12, 8))
            plt.title(f'Returns: {self._ticker}', fontsize=15)
            # plt.show()
        elif kind == 'hist':
            self.data.log_returns.hist(figsize=(12, 8), bins=int(np.sqrt(len(self.data))))
            plt.title(f'Frequency of Returns: {self._ticker}', fontsize=15)
            # plt.show()

stock = FinancialInstrument('AAPL', '2015-01-01', '2019-12-31')
print(stock)
# print(stock._ticker)
# print(stock.data)
# stock.data.log_returns.plot()
# plt.show()
# stock.data.log_returns.hist(bins=100)
# plt.show()
# stock.plot_prices()
# stock.plot_return()

