# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import time
#
#
# class IterativeBase():
#
#     def __init__(self, symbol, start, end, amount, use_spread=True):
#         self.symbol = symbol
#         self.start = start
#         self.end = end
#         self.initial_balance = amount
#         self.current_balance = amount
#         self.units = 0
#         self.trades = 0
#         self.position = 0
#         self.use_spread = use_spread
#         self.get_data()
#
#     def get_data(self):
#         raw = pd.read_csv("../Materials/detailed.csv", parse_dates=["time"], index_col="time").dropna()
#         raw = raw.loc[self.start:self.end]
#         raw["returns"] = np.log(raw.price / raw.price.shift(1))
#         self.data = raw
#
#     def plot_data(self, cols=None):
#         if cols is None:
#             cols = "price"
#         self.data[cols].plot(figsize=(12, 8), title=self.symbol)
#
#     def get_values(self, bar):
#         date = str(self.data.index[bar].date())
#         price = round(self.data.price.iloc[bar], 5)
#         spread = round(self.data.spread.iloc[bar], 5)
#         return date, price, spread
#
#     def print_current_balance(self, bar):
#         date, price, spread = self.get_values(bar)
#         print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))
#
#     def buy_instrument(self, bar, units=None, amount=None):
#         date, price, spread = self.get_values(bar)
#         if self.use_spread:
#             price += spread/2  # ask price
#         if amount is not None:  # use units if units are passed, otherwise calculate units
#             units = int(amount / price)
#         self.current_balance -= units * price  # reduce cash balance by "purchase price"
#         self.units += units
#         self.trades += 1
#         print("{} |  Buying {} for {}".format(date, units, round(price, 5)))
#
#     def sell_instrument(self, bar, units=None, amount=None):
#         date, price, spread = self.get_values(bar)
#         if self.use_spread:
#             price -= spread/2  # bid price
#         if amount is not None:  # use units if units are passed, otherwise calculate units
#             units = int(amount / price)
#         self.current_balance += units * price  # increases cash balance by "purchase price"
#         self.units -= units
#         self.trades += 1
#         print("{} |  Selling {} for {}".format(date, units, round(price, 5)))
#
#     def print_current_position_value(self, bar):
#         date, price, spread = self.get_values(bar)
#         cpv = self.units * price
#         print("{} |  Current Position Value = {}".format(date, round(cpv, 2)))
#
#     def print_current_nav(self, bar):
#         date, price, spread = self.get_values(bar)
#         nav = self.current_balance + self.units * price
#         print("{} |  Net Asset Value = {}".format(date, round(nav, 2)))
#
#     def close_pos(self, bar):
#         date, price, spread = self.get_values(bar)
#         print(75 * "-")
#         print("{} | +++ CLOSING FINAL POSITION +++".format(date))
#         self.current_balance += self.units * price  # closing final position (works with short and long!)
#         self.current_balance -= (abs(self.units)*spread/2*self.use_spread)
#         print("{} | closing position of {} for {}".format(date, self.units, price))
#         self.units = 0  # setting position to neutral
#         self.trades += 1
#         perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
#         self.print_current_balance(bar)
#         print("{} | net performance (%) = {}".format(date, round(perf, 2)))
#         print("{} | number of trades executed = {}".format(date, self.trades))
#         print(75 * "-")
#
#
# class IterativeBacktest(IterativeBase):
#
#     # helper method
#     def go_long(self, bar, units=None, amount=None):
#         if self.position == -1:
#             self.buy_instrument(bar, units=-self.units)  # if short position, go neutral first
#         if units:
#             self.buy_instrument(bar, units=units)
#         elif amount:
#             if amount == "all":
#                 amount = self.current_balance
#             self.buy_instrument(bar, amount=amount)  # go long
#
#     # helper method
#     def go_short(self, bar, units=None, amount=None):
#         if self.position == 1:
#             self.sell_instrument(bar, units=self.units)  # if long position, go neutral first
#         if units:
#             self.sell_instrument(bar, units=units)
#         elif amount:
#             if amount == "all":
#                 amount = self.current_balance
#             self.sell_instrument(bar, amount=amount)  # go short
#
#     def test_sma_strategy(self, SMA_S, SMA_L):
#
#         # nice printout
#         stm = "Testing SMA strategy | {} | SMA_S = {} & SMA_L = {}".format(self.symbol, SMA_S, SMA_L)
#         print("-" * 75)
#         print(stm)
#         print("-" * 75)
#
#         # reset
#         self.position = 0  # initial neutral position
#         self.trades = 0  # no trades yet
#         self.current_balance = self.initial_balance  # reset initial capital
#         self.get_data()  # reset dataset
#
#         # prepare data
#         self.data["SMA_S"] = self.data["price"].rolling(SMA_S).mean()
#         self.data["SMA_L"] = self.data["price"].rolling(SMA_L).mean()
#         self.data.dropna(inplace=True)
#
#         # sma crossover strategy
#         for bar in range(len(self.data) - 1):  # all bars (except the last bar)
#             if self.data["SMA_S"].iloc[bar] > self.data["SMA_L"].iloc[bar]:  # signal to go long
#                 if self.position in [0, -1]:
#                     self.go_long(bar, amount="all")  # go long with full amount
#                     self.position = 1  # long position
#             elif self.data["SMA_S"].iloc[bar] < self.data["SMA_L"].iloc[bar]:  # signal to go short
#                 if self.position in [0, 1]:
#                     self.go_short(bar, amount="all")  # go short with full amount
#                     self.position = -1  # short position
#         self.close_pos(bar + 1)  # close position at the last bar
#
#
# bc = IterativeBacktest("EURUSD", "2006-12-31", "2020-06-30", 100000, use_spread = True)
#
# bc.test_sma_strategy(50, 200)

# plt.style.use('seaborn')
#
# data = pd.read_csv("../Materials/detailed.csv", parse_dates=["time"], index_col="time")
# data = data.round(5)

# data.price.plot(figsize=(12, 8))
# plt.show()
# data.spread.hist(bins=100, figsize=(12, 8))
# plt.show()
#
# for bar in range(10):
#     print(bar, data.index[bar].date(), data.price[bar], data.spread[bar], sep=" | ")

# sma_s = 50
# sma_l = 200
#
# data["SMA_S"] = data.price.rolling(sma_s).mean()
# data["SMA_L"] = data.price.rolling(sma_l).mean()
#
# data.dropna(inplace=True)
# print(data)
# position = 0
# for bar in range(len(data)):
#     if data["SMA_S"].iloc[bar] > data["SMA_L"].iloc[bar]:
#         if position in [0, -1]:
#             print("{}: Go Long  | Price: {} | Spread: {}".format(data.index[bar].date(), data.price[bar],
#                                                                  data.spread[bar]))
#             position = 1
#     elif data["SMA_S"].iloc[bar] < data["SMA_L"].iloc[bar]:
#         if position in [0, 1]:
#             print("{}: Go Short | Price: {} | Spread: {}".format(data.index[bar].date(), data.price[bar],
#                                                                  data.spread[bar]))
#             position = -1
