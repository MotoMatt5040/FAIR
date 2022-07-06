import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
plt.style.use('seaborn')
lm = LinearRegression(fit_intercept=True)

# budget = np.array([5, 10, 17, 27, 35, 40, 42, 49, 54, 60])
# revenue = np.array([2.6, 19., 23.8, 26.9, 41.1, 58.3, 40.3, 58.7, 73.1, 69.7])
#
# df = pd.DataFrame(data={'revenue': revenue, 'budget': budget})
# print(df)
#
# plt.figure(figsize=(12, 8))
# plt.scatter(x=df.budget, y=df.revenue, s=50)
# plt.xlabel('Budget', fontsize=13)
# plt.ylabel('Revenue', fontsize=13)
# plt.show()
#
#
# lm.fit(X=df.budget.to_frame(), y=df.revenue)
# slope = lm.coef_
# print(slope)
# intercept = lm.intercept_
# print(intercept)
# df['pred'] = lm.predict(df.budget.to_frame())
# print(df)
# #
# x_lin = np.array([0, 100])
# y_lin = intercept + slope * x_lin
#
# budget_new = np.array([63, 66, 74, 80, 85])
# revenue_new = np.array([74.2, 80.7, 98.2, 94.8, 101.7])
#
# df_new = pd.DataFrame(data={'revenue': revenue_new, 'budget': budget_new})
#
# df_new['pred'] = lm.predict(df_new.budget.to_frame())
#
# print(df_new)
#
# # Overfitting
# poly_m = np.polyfit(x=df.budget, y=df.revenue, deg=9)
# print(poly_m)
# x_poly = np.linspace(0, 100, 1000)
# y_poly = np.polyval(poly_m, x_poly)
#
# # Underfitting
# mean = df.revenue.mean()
# print(mean)
#
# plt.figure(figsize=(12, 8))
# plt.scatter(x=df.budget, y=df.revenue, s=50, label='Data')
# plt.plot(x_lin, y_lin, c='red', label='Regression Line')
# plt.plot(x_poly, y_poly, label='Polynomial Regression | deg=9 (Overfit)', linestyle='--', color='red')
# plt.hlines(y=mean, xmin=0, xmax=100, linestyle='-.', color='darkred', label='Underfit')
# plt.scatter(x=df_new.budget, y=df_new.revenue, s=50, label='New Data')
# plt.xlabel('Budget', fontsize=13)
# plt.ylabel('Revenue', fontsize=13)
# plt.legend(fontsize=13)
# plt.ylim(0, 150)
# plt.show()

# data = pd.read_csv('../Materials/five_minute.csv', parse_dates=['time'], index_col='time')
# # data.plot(figsize=(12, 8))
# # plt.show()
#
# data['returns'] = np.log(data.div(data.shift(1)))

# # Simple linear regression model
# data['lag1'] = data.returns.shift(1)
# data.dropna(inplace=True)
# print(data)
#
# lm.fit(X=data.lag1.to_frame(), y=data.returns)
# slope = lm.coef_
# intercept = lm.intercept_
# data['pred'] = lm.predict(data.lag1.to_frame())
# print(data)
#
#
# # data.iloc[: -2:].plot(kind='scatter', x='lag1', y='returns')
# # plt.scatter(x=data.lag1, y=data.returns, label='Data')
# # plt.plot(data.lag1, data.pred, c='red', label='Linear Regression')
# # plt.xlim(-0.005, 0.005)
# # plt.ylim(-0.005, 0.005)
# # plt.xlabel('Lag1 Returns', fontsize=13)
# # plt.ylabel('Returns', fontsize=13)
# # plt.show()
#
# # data[['returns', 'pred']].plot(figsize=(12, 8))
# # plt.show()
# data.pred = np.sign(data.pred)
# print(data)
# # print(np.sign(data.returns * data.pred))
# # print(data)
#
# hits = np.sign(data.returns * data.pred).value_counts()
# print(hits)
# hit_ratio = hits[1.0] / sum(hits)
# print(hit_ratio)


data = pd.read_csv('../Materials/five_minute.csv', parse_dates=['time'], index_col='time')

data['returns'] = np.log(data.div(data.shift(1)))

lags = 5
cols = []
for lag in range(1, lags+1):
    col = f'lag{lag}'
    data[col] = data.returns.shift(lag)
    cols.append(col)
data.dropna(inplace=True)


lm.fit(data[cols], data.returns)

data['pred'] = lm.predict(data[cols].values)
data.pred = np.sign(data.pred)
hits = np.sign(data.returns * data.pred).value_counts()
hit_ratio = hits[1.0] / sum(hits)
print(data[:10].to_string())
print(data.pred.value_counts())
print(hits)
print(hit_ratio)

data['strategy'] = data.pred * data.returns
data['creturns'] = data['returns'].cumsum().apply(np.exp)
data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)

data[['creturns', 'cstrategy']].plot(figsize=(12, 8))
plt.show()

data['trades'] = data.pred.diff().fillna(0).abs()
print(data.trades.value_counts())

# forward testing #####################################################################################################
data = pd.read_csv('../Materials/test_set.csv', parse_dates=['time'], index_col='time')
data['returns'] = np.log(data.div(data.shift(1)))

lags = 5
cols = []
for lag in range(1, lags+1):
    col = f'lag{lag}'
    data[col] = data.returns.shift(lag)
    cols.append(col)
data.dropna(inplace=True)
data['pred'] = lm.predict(data[cols].values)
data.pred = np.sign(data.pred)
hits = np.sign(data.returns * data.pred).value_counts()
hit_ratio = hits[1.0] / sum(hits)
print(data[:10].to_string())
print(data.pred.value_counts())
print(hits)
print(hit_ratio)
data['strategy'] = data.pred * data.returns
data['creturns'] = data['returns'].cumsum().apply(np.exp)
data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
data[['creturns', 'cstrategy']].plot(figsize=(12, 8))
plt.show()

data['trades'] = data.pred.diff().fillna(0).abs()
print(data.trades.value_counts())




