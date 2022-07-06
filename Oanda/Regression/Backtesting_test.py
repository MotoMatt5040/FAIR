import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

plt.style.use("seaborn")
df = pd.read_csv("../Materials/five_minute_pairs.csv", parse_dates=["time"], index_col="time")
import MLBacktester as MLB

# EURUSD
symbol = "EURUSD"
ptc = 0.00007
ml = MLB.MLBacktester(symbol, "2019-01-01", "2020-08-31", ptc)
print(ml)
print(ml.data)
print(ml.test_strategy(train_ratio=0.7, lags=5))
ml.plot_results()
plt.show()
print(ml.results)

# The optimal Number of Lags
for lags in range(1, 21):
    print(lags, ml.test_strategy(train_ratio=0.7, lags=lags))
ml.results.trades.value_counts()

# EURAUD
symbol = "EURAUD"
ml = MLB.MLBacktester(symbol, "2019-01-01", "2020-08-31", 0)
ml.test_strategy(train_ratio=0.7, lags=15)
ml.plot_results()
plt.show()

# The optimal Number of Lags
for lags in range(1, 21):
    print(lags, ml.test_strategy(train_ratio=0.7, lags=lags))
print(ml.results)
hits = np.sign(ml.results.returns * ml.results.pred).value_counts()
print(hits)
hit_ratio = hits[1.0] / sum(hits)
print(hit_ratio)
