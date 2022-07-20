import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")
data = pd.read_csv("Materials/intraday.csv", parse_dates=["time"], index_col="time")
data.info()
# data.plot(figsize=(12, 8))
# plt.show()
# data.loc["2019-08"].plot(figsize=(12, 8))
# plt.show()
data["returns"] = np.log(data.div(data.shift(1)))
# Defining a Mean-Reversion Strategy (Bollinger Bands) (Part 1)
# Mean Reversion: Financial Instruments are from time to time overbought / oversold and revert back to mean prices.
#
# Bollinger Bands: Consists of a SMA (e.g. 30) and Upper and Lower Bands +- (2) Std Dev away from SMA.

SMA = 30
dev = 1
# data["SMA"] = data["price"].rolling(SMA).mean()
# # data[["price", "SMA"]].plot(figsize=(12, 8))
# # plt.show()
# # data.loc["2019-08", ["price", "SMA"]].plot(figsize=(12, 8))
# # plt.show()
# data["price"].rolling(SMA).std()
# data["price"].rolling(SMA).std().plot(figsize=(12, 8))
# plt.show()
# data["Lower"] = data["SMA"] - data["price"].rolling(SMA).std() * dev  # Lower Band -2 Std Dev
# data["Upper"] = data["SMA"] + data["price"].rolling(SMA).std() * dev  # Upper Band -2 Std Dev
# # data.drop(columns="returns").plot(figsize=(12, 8))
# # plt.show()
# # data.drop(columns="returns").loc["2019-08"].plot(figsize=(12, 8))
# # plt.show()
# data.dropna(inplace=True)
# 
# # Defining a Mean-Reversion Strategy (Bollinger Bands) (Part 2)
# 
# data["distance"] = data.price - data.SMA  # helper Column
# data["position"] = np.where(data.price < data.Lower, 1, np.nan)  # 1. oversold -> go long
# data["position"] = np.where(data.price > data.Upper, -1, data["position"])  # 2. overbought -> go short
# 
# # 3. crossing SMA ("Middle Band") -> go neutral
# data["position"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["position"])
# 
# data["position"] = data.position.ffill().fillna(0)  # where 1-3 isn´t applicable -> hold previous position
# data.position.value_counts()
# data.drop(columns=["returns", "distance"]).loc["2019-08"].plot(figsize=(12, 8), secondary_y="position")
# plt.show()
# data.position.plot(figsize=(12, 8))
# plt.show()

price = 'price'
smas = 47
smal = 162
sma = 43
dev = 2

#SMA Crossover
data['SMAS'] = data[price].rolling(smas).mean()
data['SMAL'] = data[price].rolling(smal).mean()
data['sposition'] = np.where(data['SMAS'] > data['SMAL'], 1, -1)

#Bollinger
data["SMA"] = data[price].rolling(sma).mean()
data["Lower"] = data["SMA"] - data[price].rolling(sma).std() * dev
data["Upper"] = data["SMA"] + data[price].rolling(sma).std() * dev
data["distance"] = data[price] - data.MSMA
data["bposition"] = np.where(data[price] < data.Lower, 1, np.nan)
data["bposition"] = np.where(data[price] > data.Upper, -1, data["bposition"])
data["bposition"] = np.where(data.distance * data.distance.shift(1) < 0, 0, data["bposition"])
data["bposition"] = data.bposition.ffill().fillna(0)

#Define position
data['position'] = np.where(data['sposition'] == data['bposition'], data['sposition'], 0)

# data.drop(columns=["returns", "distance"]).plot(figsize=(12, 8), secondary_y="position")
# plt.show()

# data.position.plot(figsize=(12, 8))
# plt.show()

# Vectorized Strategy Backtesting

data["strategy"] = data.position.shift(1) * data["returns"]
data.dropna(inplace=True)

data["creturns"] = data["returns"].cumsum().apply(np.exp)
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
# data[["creturns", "cstrategy"]].plot(figsize=(12, 8))
# plt.show()

ptc = 0.00007
data["trades"] = data.position.diff().fillna(0).abs()

data.trades.value_counts()
data["strategy_net"] = data.strategy - data.trades * ptc
data["cstrategy_net"] = data.strategy_net.cumsum().apply(np.exp)


data[["returns", "strategy_net"]].mean() * (4 * 252)  # annualized return
data[["returns", "strategy_net"]].std() * np.sqrt(4 * 252)  # annualized risk

data[['price','SMAS', 'SMAL']].plot(figsize=(12, 8), secondary_y="position")
plt.show()
data[['SMA', 'Upper', 'Lower', 'price']].plot(figsize=(12, 8), secondary_y="position")
plt.show()
data[["creturns", "cstrategy", "cstrategy_net"]].plot(figsize=(12, 8))
plt.show()

