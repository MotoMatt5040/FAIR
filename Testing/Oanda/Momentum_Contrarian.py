import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tpqoa
from itertools import product
plt.style.use('seaborn')

candle_count = 3

# api = tpqoa.tpqoa('oanda.cfg')

# df = api.get_history(instrument='EUR_USD', start='2021-01-14', end='2021-01-15', granularity='M5', price='B')
# print(df)
# close = df.c.to_frame()
# print(close)

data = pd.read_csv('Materials/intraday.csv', parse_dates=['time'], index_col='time')
# print(data.info())

data.plot(figsize=(12, 8), title='EUR/USD', fontsize=12)
# plt.show()

data.loc['2019-06'].plot(figsize=(12, 8), title='EUR/USD', fontsize=12)
# plt.show()

data['returns'] = np.log(data.div(data.shift(1)))
data.dropna(inplace=True)

# data['position'] = np.sign(data['returns'].rolling(candle_count).mean())  # positive and for momentum
data['position'] = -np.sign(data['returns'].rolling(candle_count).mean())  # negative is for contratian


#  how to backtest ->
data['strategy'] = data.position.shift(1) * data['returns']
data.dropna(inplace=True)
# print(data.head(10).to_string())

print(data[['returns', 'position']].sum())
print(data[['returns', 'position']].sum().apply(np.exp))

data['creturns'] = data['returns'].cumsum().apply(np.exp)
data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)

print(data.head(10).to_string())
