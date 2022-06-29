import pandas as pd
import numpy as np
from datetime import timedelta, date
import tpqoa
import yfinance as yf
import matplotlib.pyplot as plt
import FinancialInstruments as fi

plt.style.use('seaborn')

api = tpqoa.tpqoa("oanda.cfg")

df = pd.read_csv('Materials/eurusd.csv', parse_dates=['Date'], index_col= 'Date')
# print(df.info())
# print(df)
# df.plot(figsize=(12, 8), title='EUR/USD', fontsize=12)
# plt.show()

df['returns'] = np.log(df.div(df.shift(1)))
df['creturns'] = df.returns.cumsum().apply(np.exp)
# print(df)

df.dropna(inplace=True)
print(f'{df}\n\n')
print(f'Percent return: {df.returns.sum()}\n\n')  # sums returns percentage
print(f'Actual dollar return: {np.exp(df.returns.sum())}\n\n')  # shows profit/loss of sums
print(f'Yearly percent return: \n{df.returns.cumsum()}\n\n')  # shows yearly return percentage
print(f'Yearly dollar returns: \n{df.returns.cumsum().apply(np.exp)}\n\n')  # Yearly dollar return value
print(f'{df.describe()}\n\n')  # description of data in table such as std dev, mean, min, max, etc
print(f'Annualized mean return: {df.returns.mean() * 252}') 
print(f'Standard Deviation of returns: {df.returns.std() * np.sqrt(252)}\n\n')
# stocks = fi.FinancialInstrumentBase('AAPL', '2015-01-01', '2018-01-01')
# print(stocks)
# print(stocks.data)

# print(api.get_account_summary())
#
# ticker = ["AAPL", "BA", "KO", 'IBM', "DIS", 'MSFT']
# stocks = yf.download(tickers=ticker, start=date.today() - timedelta(365), end=date.today())
# # print(stocks.to_string())
# stocks.to_csv('stocks.csv')
# stocks = pd.read_csv('stocks.csv', header=[0, 1], index_col=[0], parse_dates=[0])
#
# # stocks = stocks.swaplevel(axis=1).sort_index(axis=1)
# print(stocks)
#
# close = stocks.loc[:, 'Close'].copy()
# print(close)
#
# ret = close.pct_change().dropna()
# print(ret)
# summary = ret.describe().T
# print(summary.to_string()) #  T Transposes the list
#
# summary['mean'] = summary['mean']*252
# summary['std'] = summary['std']* np.sqrt(252)
#
# print(summary.to_string()) #  T Transposes the list

# norm = close.div(close.iloc[0]).mul(100)
# norm.plot(figsize=(15, 8), fontsize=13)
# close.plot(figsize=(15, 8), fontsize=13)
# plt.legend(fontsize=13)
# plt.show()

# summary = api.get_account_summary()
# for item in summary:
#     print(f'{item}: {summary[item]}')
# # print(api.get_account_summary().keys())
# print(api.account_type)
# print(api.account_id)
# instruments = api.get_instruments()
# for item in instruments:
#     print(item)
# instr = api.get_instruments()
# print(len(instr))
# print(instr[0])

# help(api.get_history)
#
# df = api.get_history(instrument = "EUR_USD", start = "2022-05-01", end = "2022-05-31",
#                 granularity = "D", price = "B")

# df.info()
# print(df.to_string())

# api.stream_data('EUR_USD', stop=10)
# api.stop_stream()

# api.create_order(instrument='EUR_USD', units=100000, sl_distance=0.1)
# summary = api.get_account_summary()
# transaction = api.get_transactions()
# api.print_transactions()
# for item in summary:
#     print(f'{item}: {summary[item]}')


# api.create_order(instrument='EUR_USD', units=-100000, sl_distance=0.1)
# summary = api.get_account_summary()
# transaction = api.get_transactions()
# api.print_transactions()
# for item in summary:
#     print(f'{item}: {summary[item]}')