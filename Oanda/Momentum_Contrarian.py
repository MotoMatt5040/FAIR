import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tpqoa
from itertools import product
plt.style.use('seaborn')

api = tpqoa.tpqoa('oanda.cfg')

df = api.get_history(instrument='EUR_USD', start='2021-01-14', end='2021-01-15', granularity='M5', price='B')
print(df)
close = df.c.to_frame()
print(close)

data = pd.read_csv('Materials/intraday.csv', parse_dates=['time'], index_col='time')
print(data.info())

data.plot(figsize=(12, 8), title='EUR/USD', fontsize=12)
# plt.show()

data.loc['2019-06'].plot(figsize=(12, 8), title='EUR/USD', fontsize=12)
# plt.show()

data['returns'] = np.log(data.div(data.shift(1)))
data.dropna(inplace=True)
print(data)
