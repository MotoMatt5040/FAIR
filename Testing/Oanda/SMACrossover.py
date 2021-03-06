import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import SMABacktester as SMA
import tpqoa

# api = tpqoa.tpqoa('oanda.cfg')

# df = api.get_history(instrument='EUR_USD', start='2022-06-29', end='2022-06-30', granularity='M5', price='B')
# print(df)
# close = df.c.to_frame()
# print(close)

# tester = SMA.SMABacktester('EURUSD=X', 50, 200, '2004-01-01', '2020-06-30')

tester = SMA.SMABacktester(instrument='EUR_USD', start='2022-06-29', end='2022-06-30', granularity='M1', price='B', SMA_S=50, SMA_L=200)
# print(tester.data)#.isna().sum() to count empty values

print(tester.test_strategy())

print(tester.optimize_parameters((1, 252, 1), (1, 252, 1)))

print(f'Absolute performance %: \n{tester.results[["returns", "strategy"]].sum()}\n\n')
print(f'Absolute performance Actual $: \n{tester.results[["returns", "strategy"]].sum().apply(np.exp)}\n\n')
print(f'Annualised return $: \n{tester.results[["returns", "strategy"]].mean() * 252}\n\n')
print(f'Annualised risk $: \n{tester.results[["returns", "strategy"]].std() * np.sqrt(252)}\n\n')

print("********************************************************\n\n")

print(f'Absolute performance %: \n{tester.results[["creturns", "cstrategy"]].sum()}\n\n')
print(f'Absolute performance Actual $: \n{tester.results[["creturns", "cstrategy"]].sum().apply(np.exp)}\n\n')
print(f'Annualised return $: \n{tester.results[["creturns", "cstrategy"]].mean() * 252}\n\n')
print(f'Annualised risk: \n{tester.results[["creturns", "cstrategy"]].std() * np.sqrt(252)}\n\n')

tester.plot_results()
plt.show()

print(tester.results_overview)



# OLD TESTING BELOW ###########################################################
#
# data = df.copy()
# sma_s = 46
# sma_l = 137
#
# # print(data.price.rolling(50))
#
# data['SMA_S'] = data.price.rolling(sma_s).mean()
# data['SMA_L'] = data.price.rolling(sma_l).mean()
#
# # print(data)
#
# # # to view the full chart
# data.plot(figsize=(12, 8), title=f'EUR / USD - SMA{sma_s} | SMA{sma_l}', fontsize=12)
# plt.legend(fontsize=12)
# plt.show()
#
# # to view a chart by year
# data.loc['2016'].plot(figsize=(12, 8), title=f'EUR / USD - SMA{sma_s} | SMA{sma_l}', fontsize=12)
# plt.legend(fontsize=12)
# plt.show()
#
# # short or long position
# data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
#
# # plot short and long positions
# data.loc[:, ['SMA_S', 'SMA_L', 'position']].plot(figsize=(12, 8), fontsize=12, secondary_y='position',
#                                                  title=f'EUR / USD - SMA{sma_s} | SMA{sma_l}')
# plt.legend(fontsize=12)
# plt.show()
#
# data['returns'] = np.log(data.price.div(data.price.shift(1)))
# data['strategy'] = data.position.shift(1) * data['returns']
#
# print(f'Absolute performance %: \n{data[["returns", "strategy"]].sum()}\n\n')
# print(f'Absolute performance Actual: \n{data[["returns", "strategy"]].sum().apply(np.exp)}\n\n')
# print(f'Annualised return: \n{data[["returns", "strategy"]].mean() * 252}\n\n')
# print(f'Annualised risk: \n{data[["returns", "strategy"]].std() * np.sqrt(252)}\n\n')
#
# data['creturns'] = data['returns'].cumsum().apply(np.exp)
# data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
#
# data.dropna(inplace=True)
#
# # plot short and long positions
# data.loc[:, ['creturns', 'cstrategy']].plot(figsize=(12, 8), fontsize=12, title=f'EUR / USD - SMA{sma_s} | SMA{sma_l}')
# plt.legend(fontsize=12)
# plt.show()
#
# outperf = data.cstrategy.iloc[-1] - data.creturns.iloc[-1]
# print(f'Outperf: {outperf}\n\n')
#
#
# print(data)
#
# # def test_strategy(SMA):
# #     data = df.copy()
# #     data['returns'] = np.log(data.price.div(data.price.shift(1)))
# #     data['SMA_S'] = data.price.rolling(int(SMA[0])).mean()
# #     data['SMA_L'] = data.price.rolling(int(SMA[1])).mean()
# #     data.dropna(inplace=True)
# #
# #     data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
# #     data['strategy'] = data.position.shift(1) * data['returns']
# #     data.dropna(inplace=True)
# #
# #     return np.exp(data['strategy'].sum())
# #
# #
# # SMA_S_range = range(1, 50, 1)
# # SMA_L_range = range(100, 252, 1)
# #
# # combinations = list(product(SMA_S_range, SMA_L_range))
# #
# # print(len(combinations))
# #
# # results = []
# # for comb in combinations:
# #     results.append(test_strategy(comb))
# #
# # # print(results)
# # print(np.max(results))
# # print(np.argmax(results))
# # print(combinations[np.argmax(results)])
# # many_results = pd.DataFrame(data=combinations, columns=['SMA_S', 'SMA_L'])
# #
# # many_results['performance'] = results
# #
# # print(many_results.nlargest(10, 'performance'))
# # print(many_results.nsmallest(10, 'performance'))
# # print(many_results)

