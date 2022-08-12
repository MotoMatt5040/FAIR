# import time
# # import SMACBacktester as smacb
# import pickle
#
# boll_updater = None
#
# sma = None
# sma_value = None
# lower = None
# upper = None
# distance = None
#
#
# def check_buy() -> bool:
#     """Function to check if the SMACrossover allows
#     a buy operation.
#
#     Returns:
#         bool: True if SMACrossover allows, false if not.
#     """
#     if sma_value == None:
#         return False
#
#     if sma_value > smas_value:
#         # print(f"Don't buy: {smal_value} > {smas_value}")
#         return False
#     elif smas_value > smal_value:
#         # print(f"Buy: {smas_value} > {smal_value}")
#         return True
#     return False
#
#
# def check_sell() -> bool:
#     """Function to check if the SMACrossover
#     allows a sell operation.
#
#     Returns:
#         bool: True if SMACrossover allows, false if not.
#     """
#     if smal_value == None or smas_value == None:
#         return False
#
#     if smal_value < smas_value:
#         # print(f"Don't sell: {smal_value} < {smas_value}")
#         return False
#     elif smas_value < smal_value:
#         # print(f"Sell: {smas_value} < {smal_value}")
#         return True
#     return False
#
#
# def SMA(ticks):
#     """Function that computes the Short Simple Moving Average.
#
#     Args:
#         ticks (list): List with prices.
#
#     Returns:
#         float: value
#     """
#     sma = boll_updater[0]
#     return sum(ticks[:sma]) / sma
#
# def LOWER(ticks):
#     sma = boll_updater[0]
#     return(sum(ticks[:sma]))
#     pass
#
# def UPPER(ticks):
#     pass
#
#
# def thread_SMAC(pill2kill, ticks: list, indicators: dict):
#     """Function executed by a thread. Calculates the SMA Short/Long and
#     stores it in the dictionary.
#
#     Args:
#         pill2kill (Threading.event): Event for stopping the threads executuion.
#         ticks (list): List with prices.
#         indicators (dict): Dictionary where the values are stored.
#     """
#
#     global sma, dev, boll_updater, sma_value
#
#     # Wait if there are not enough elements
#     while len(ticks) < 70 and not pill2kill.wait(1.5):
#         print("[THREAD - BOLL] - Waiting for ticks\n")
#         # tester = smacb.SMACBacktester(ticks=ticks)
#         # print(tester.optimize_parameters((1, 20, 1), (21, 70, 1)))
#         # sma_updater = pickle.load(open("sma_update.pkl", "rb"))
#         # print(f't {ticks}')
#
#     print("[THREAD - BOLL] - Computing values\n")
#     boll_updater = pickle.load(open("boll_update.pkl", "rb"))
#     sma = boll_updater[0]
#
#     while not pill2kill.wait(1):
#         sma_value = SMA(ticks[::-1])
#         indicators['BOLL']['SMA'] = sma_value
#
#
# def thread_SMAC_update(pill2kill, ticks: list, indicators: dict):
#     """Function executed by a thread. Calculates the SMA Short/Long and
#     stores it in the dictionary.
#
#     Args:
#         pill2kill (Threading.event): Event for stopping the threads executuion.
#         ticks (list): List with prices.
#         indicators (dict): Dictionary where the values are stored.
#     """
#
#     global smas, dev, boll_updater, sma_value
#
#     # Wait if there are not enough elements
#     while len(ticks) < 70 and not pill2kill.wait(1.5):
#         print("[THREAD - BOLL] - Waiting for ticks\n")
#
#     print("[THREAD - BOLL] - Computing values\n")
#     # tester = smacb.SMACBacktester(ticks=ticks)
#
#
#     while not pill2kill.wait(900):
#         # print(tester.optimize_parameters((1, 20, 1), (21, 70, 1)))
#         # sma_updater = pickle.load(open("boll_update.pkl", "rb"))
#         sma = boll_updater[0]
#         sma_value = SMA(ticks[::-1])
#         indicators['BOLL']['SMA'] = sma_value
#
