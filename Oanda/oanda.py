import ConTrader as ct
import SMACTrader as st
import BollTrader as bt
import MLTrader as mt
import SMABacktester as smabt
import pickle
import time
from sklearn.linear_model import LogisticRegression
from datetime import date, timedelta


# contrader = ct.ConTrader("oanda.cfg", "EUR_USD", "1min", window=1, units=100000)

bolltrader = bt.BollTrader("oanda.cfg", "EUR_USD", "1min", sma=10, dev=2, units=100000)

# lm = pickle.load(open("logreg.pkl", "rb"))
# lags = pickle.load(open("lags.pkl", "rb"))
# granularity = pickle.load(open("granularity.pkl", "rb"))

# sma_updater = pickle.load(open("sma_update.pkl", "rb"))
# print(sma_updater, sma_updater[0], sma_updater[1])

# smatrader = st.SMACTrader("oanda.cfg", "EUR_USD", "1min", smas=sma_updater[0], smal=sma_updater[1], units=100000)
# smau = smabt.SMABacktester(instrument='EUR_USD', start=str(date.today() - timedelta(1)), end=str(date.today()), granularity='M1', price='B', SMA_S=37, SMA_L=1)

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

# def sma_update():
#     print(smau.optimize_parameters((1, 50, 1), (51, 170, 1))[0])
#
#
# def sma_trading():
#     while True:
#         try:
#             sma_update()
#             smatrader.get_most_recent()
#             smatrader.stream_data(smatrader.instrument)  # , stop=20000
#             if smatrader.position != 0:  # if we have a final open position
#                 close_order = smatrader.create_order(smatrader.instrument, units=-smatrader.position * smatrader.units,
#                                                      suppress=True, ret=True)
#                 smatrader.report_trade(close_order, "GOING NEUTRAL")
#                 smatrader.position = 0
#         except Exception as err:
#             print(err)
#             time.sleep(900)

def boll_trading():
    while True:
        try:
            bolltrader.get_most_recent()
            bolltrader.stream_data(bolltrader.instrument)  # , stop=20000
            if bolltrader.position != 0:  # if we have a final open position
                close_order = bolltrader.create_order(bolltrader.instrument, units=-bolltrader.position * bolltrader.units,
                                                      suppress=True, ret=True)
                bolltrader.report_trade(close_order, "GOING NEUTRAL")
                bolltrader.position = 0
        except Exception as err:
            print(err)
            time.sleep(900)


if __name__ == '__main__':
    # sma_trading()
    boll_trading()


# pickle.dump(trader.model, open("logreg.pkl", "wb"))


