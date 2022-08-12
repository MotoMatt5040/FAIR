# import ConTrader as ct
# import SMACTrader as st
# import BollTrader as bt
# import MLTrader as mt
# import SMABacktester as smabt
# import pickle
# import time
# from sklearn.linear_model import LogisticRegression
# from datetime import date, timedelta, datetime
#
#
# contrader = ct.ConTrader("oanda.cfg", "EUR_USD", "1min", window=1, units=100000)
#
# bolltrader = bt.BollTrader("oanda.cfg", "EUR_USD", "1min", sma=20, dev=1, units=100000)
#
# lm = pickle.load(open("logreg.pkl", "rb"))
# lags = pickle.load(open("lags.pkl", "rb"))
# granularity = pickle.load(open("granularity.pkl", "rb"))
#
# sma_updater = pickle.load(open("sma_update.pkl", "rb"))
# print(sma_updater, sma_updater[0], sma_updater[1])
#
# YYYY-MM-DDTHH:MM:SS
# print(str(datetime.now() - timedelta(hours=1))[:-7])
# print(datetime.now())
#
# smatrader = st.SMACTrader("oanda.cfg", "AUD_USD", "15min", smas=sma_updater[0], smal=sma_updater[1], units=500000)
# smau = smabt.SMABacktester(instrument='EUR_USD', start=str(date.today() - timedelta(1)), end=str(date.today()), granularity='M1', price='B', SMA_S=37, SMA_L=1)
# smau = smabt.SMABacktester(instrument='EUR_USD', start=str(datetime.now() - timedelta(days=7))[:-7],
#                            end=str(datetime.now())[:-7], granularity='M15', price='B', SMA_S=37, SMA_L=1)
#
#
# def sma_update():
#     print(smau.optimize_parameters((1, 20, 1), (21, 100, 1))[0])
#     smau.plot_results()
#
#
# def sma_trading():
#     while True:
#         try:
#         sma_update()
#         smatrader.get_most_recent()
#         smatrader.stream_data(smatrader.instrument)  # , stop=20000
#         if smatrader.position != 0:  # if we have a final open position
#             close_order = smatrader.create_order(smatrader.instrument, units=-smatrader.position * smatrader.units,
#                                                  suppress=True, ret=True)
#             smatrader.report_trade(close_order, "GOING NEUTRAL")
#             smatrader.position = 0
#         except Exception as err:
#             print(err)
#             time.sleep(1)
#
#
# print(lags, type(lags), granularity, type(granularity), sep=', ')
#
#
# trader = mt.MLTrader("oanda.cfg", "EUR_USD", "15min", model=lm, lags=lags, granularity='S5', units=100000)
#
# def ml_trading():
#     while True:
#         try:
#             trader.get_most_recent()
#             trader.stream_data(trader.instrument, stop=20000)
#             if trader.position != 0:  # if we have a final open position
#                 close_order = trader.create_order(trader.instrument, units=-trader.position * trader.units,
#                                                   suppress=True, ret=True)
#                 trader.report_trade(close_order, "GOING NEUTRAL")
#                 trader.position = 0
#         except Exception as err:
#             print(err)
#
# if __name__ == '__main__':
#     sma_trading()
#     ml_trading()
#
# pickle.dump(trader.model, open("logreg.pkl", "wb"))


