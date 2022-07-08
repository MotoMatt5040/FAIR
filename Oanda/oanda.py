import ConTrader as ct
import SMACTrader as st
import BollTrader as bt
import MLTrader as mt
import pickle
from sklearn.linear_model import LogisticRegression


# trader = ct.ConTrader("oanda.cfg", "EUR_USD", "1min", window=1, units=100000)
# trader = st.SMACTrader("oanda.cfg", "EUR_USD", "1min", smas=50, smal=200, units=100000)
# trader = bt.BollTrader("oanda.cfg", "EUR_USD", "1min", sma=20, dev=1, units=100000)

lm = pickle.load(open("logreg.pkl", "rb"))
lags = pickle.load(open("lags.pkl", "rb"))
granularity = pickle.load(open("granularity.pkl", "rb"))
trader = mt.MLTrader("oanda.cfg", "EUR_USD", "5min", model=lm, lags=lags, granularity=granularity, units=100000)

trader.get_most_recent()
trader.stream_data(trader.instrument, stop=2000)
if trader.position != 0:  # if we have a final open position
    close_order = trader.create_order(trader.instrument, units=-trader.position * trader.units,
                                      suppress=True, ret=True)
    trader.report_trade(close_order, "GOING NEUTRAL")
    trader.position = 0

pickle.dump(trader.model, open("logreg.pkl", "wb"))

