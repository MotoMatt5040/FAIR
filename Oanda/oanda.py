import ConTrader as ct
import SMACTrader as st
import BollTrader as bt
import MLTrader as mt
import pickle
import time
from sklearn.linear_model import LogisticRegression


# contrader = ct.ConTrader("oanda.cfg", "EUR_USD", "1min", window=1, units=100000)

# bolltrader = bt.BollTrader("oanda.cfg", "EUR_USD", "1min", sma=20, dev=1, units=100000)

# lm = pickle.load(open("logreg.pkl", "rb"))
# lags = pickle.load(open("lags.pkl", "rb"))
# granularity = pickle.load(open("granularity.pkl", "rb"))

# print(lags, type(lags), granularity, type(granularity), sep=', ')


# trader = mt.MLTrader("oanda.cfg", "EUR_USD", "5min", model=lm, lags=lags, granularity='S5', units=100000)
#
# trader.get_most_recent()
# trader.stream_data(trader.instrument, stop=20000)
# if trader.position != 0:  # if we have a final open position
#     close_order = trader.create_order(trader.instrument, units=-trader.position * trader.units,
#                                       suppress=True, ret=True)
#     trader.report_trade(close_order, "GOING NEUTRAL")
#     trader.position = 0

smatrader = st.SMACTrader("oanda.cfg", "EUR_USD", "1min", smas=37, smal=1, units=100000)

smatrader.get_most_recent()
smatrader.stream_data(smatrader.instrument)  #, stop=20000
if smatrader.position != 0:  # if we have a final open position
    close_order = smatrader.create_order(smatrader.instrument, units=-smatrader.position * smatrader.units,
                                      suppress=True, ret=True)
    smatrader.report_trade(close_order, "GOING NEUTRAL")
    smatrader.position = 0

# pickle.dump(trader.model, open("logreg.pkl", "wb"))


