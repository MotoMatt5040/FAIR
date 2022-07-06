import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score

plt.style.use('seaborn')
# lm = LinearRegression(fit_intercept= True)
lm = LogisticRegression()

# hours = np.array([0.5, 0.75, 1., 1.25, 1.5, 1.75, 1.75, 2.,
#                   2.25, 2.5, 2.75, 3., 3.25, 3.5, 4., 4.25,
#                   4.5, 4.75, 5., 5.5])
#
# success = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])
#
# data = pd.DataFrame({'hours': hours, 'success': success})
#
# # lm.fit(data.hours.to_frame(), data.success)
# # data["pred"] = lm.predict(data.hours.to_frame())
# #
# # print(data.to_string())
# #
# # plt.figure(figsize=(12, 6))
# # plt.scatter(hours, success)
# # plt.xlabel("Study Hours", fontsize = 15)
# # plt.ylabel("Pass/Fail", fontsize = 15)
# # plt.ylim(-0.2, 1.2)
# # plt.show()
#
#
# lm.fit(data.hours.to_frame(), data.success)
# data["pred"] = lm.predict(data.hours.to_frame())
#
# print(data.to_string())
#
# proba = lm.predict_proba(data.hours.to_frame())
# print(proba)
#
# plt.figure(figsize=(12, 6))
# plt.scatter(data.hours, data.success, label="Data")
# plt.plot(data.hours, data.pred, color="red", label="Classification")
# plt.plot(data.hours, proba[:, 0], "m--", label="Probability Fail")
# plt.plot(data.hours, proba[:, 1], "g--", label="Probability Pass")
# plt.legend(fontsize=13)
# plt.yticks(np.arange(-0.2, 1.3, 0.1))
# plt.ylim(-0.2, 1.2)
# plt.xlabel("Study Hours", fontsize=15)
# plt.ylabel("Pass/Fail", fontsize=15)
# plt.show()

print(f'\n********************************Backtesting********************************\n')
data = pd.read_csv("../Materials/five_minute.csv", parse_dates=["time"], index_col="time")
data["returns"] = np.log(data.div(data.shift(1)))
data.dropna(inplace=True)
data["direction"] = np.sign(data.returns)

print(data.direction.value_counts())

lags = 5
cols = []
for lag in range(1, lags + 1):
    col = "lag{}".format(lag)
    data[col] = data.returns.shift(lag)
    cols.append(col)
data.dropna(inplace=True)

lm = LogisticRegression(C=1e6, max_iter=100000, multi_class="ovr")
lm.fit(data[cols], data.direction)
data["pred"] = lm.predict(data[cols])
hits = np.sign(data.direction * data.pred).value_counts()
hit_ratio = hits[1.0] / sum(hits)

print(hits, hit_ratio)
print(accuracy_score(y_true=data.direction, y_pred=data.pred))

# In-Sample backtest - if the data performs much better in the backtest then there is overfitting.
# adjust the logistic regression c value to a higher value in this case to decrease regularization
data["strategy"] = data.pred * data.returns
data["creturns"] = data["returns"].cumsum().apply(np.exp)
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)

data[["creturns", "cstrategy"]].plot(figsize=(12, 8))
plt.show()

data["trades"] = data.pred.diff().fillna(0).abs()
print(data.trades.value_counts())

# Out-Sample forward testing
print(f'\n********************************Forward Testing********************************\n')
data = pd.read_csv("../Materials/test_set.csv", parse_dates=["time"], index_col="time")

data["returns"] = np.log(data.div(data.shift(1)))
data["direction"] = np.sign(data.returns)
lags = 5
cols = []
for lag in range(1, lags + 1):
    col = "lag{}".format(lag)
    data[col] = data.returns.shift(lag)
    cols.append(col)
data.dropna(inplace=True)
data["pred"] = lm.predict(data[cols])

print(data.pred.value_counts())

hits = np.sign(data.direction * data.pred).value_counts()
hit_ratio = hits[1.0] / sum(hits)

print(hits, hit_ratio)

data["strategy"] = data.pred * data.returns

data["creturns"] = data["returns"].cumsum().apply(np.exp)
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)

data[["creturns", "cstrategy"]].plot(figsize=(12, 8))
plt.show()

data["trades"] = data.pred.diff().fillna(0).abs()

data.trades.value_counts()

print(data.trades.value_counts())
