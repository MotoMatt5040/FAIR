# FAIR (Forex AI Repository) Project
# V 2.0
# 5/10/2022

import logging
import time

import keyboard

import bot

# logging.basicConfig(level=logging.DEBUG)
# logging.root.setLevel(logging.DEBUG)
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
# file_handler = logging.FileHandler('../logs/main.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.propagate = False

# Creating a bot
# TODO Fix bot statement
b = bot.Bot(0.01, 60, "EURUSD")
# b = bot.Bot(5.0, 60 * 15, "USDJPY!")

# markets = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']

# for market in markets:


# with open("login_data.txt", 'r') as f:
#     lines = f.readlines()
#     usr = int(lines[0])
#     password = lines[1]

# print('''Which account would you like to use
#     1: MT5 Demo
#     2: Hanko Demo
#     3: Traders Domain - Live
#     4: Vital Markets - Demo
#     5: Vital Markets - Live''')
# usr = None
# password = None
# while usr is None or password is None:
#     if keyboard.is_pressed('1'):
#         usr = 5003534489
#         password = '6jsxifbk'
#         print(f'\nYou selected: {usr}\n')
#     elif keyboard.is_pressed('2'):
#         usr = 805062
#         password = 'R6rz@i@Ue!#bCAn'
#         print(f'\nYou selected: {usr}\n')
#     elif keyboard.is_pressed('3'):
#         usr = 10035241
#         password = 'R3k5tpbz'
#         print(f'\nYou selected: {usr}\n')
#     elif keyboard.is_pressed('4'):
#         usr = 182963
#         password = 'GQhPJhcFAT'
#         print(f'\nYou selected: {usr}\n')
#     elif keyboard.is_pressed('5'):
#         usr = 10024028
#         password = 'qMnkbKzXHG'
#         print(f'\nYou selected: {usr}\n')
#
# time.sleep(0.1)
# print('''Which server would you like to connect to?
#     1: MetaQuotes-Demo
#     2: OANDA-Demo-2
#     3: TradersDomainFX-MetaTrader5
#     4: VitalMarkets-Demo
#     5: VitalMarkets-Live''')
# server = None
# while server is None:
#     if keyboard.is_pressed('1'):
#         server = 'MetaQuotes-Demo'
#         print(f'\nYou selected: {server}\n')
#     elif keyboard.is_pressed('2'):
#         server = 'OANDA-Demo-2'
#         print(f'\nYou selected: {server}\n')
#     elif keyboard.is_pressed('3'):
#         server = 'TradersDomainFX-MetaTrader5'
#         print(f'\nYou selected: {server}\n')
#     elif keyboard.is_pressed('4'):
#         server = 'VitalMarkets-Demo'
#         print(f'\nYou selected: {server}\n')
#     elif keyboard.is_pressed('5'):
#         server = 'VitalMarkets-Live'
#         print(f'\nYou selected: {server}\n')

usr = 10024165
password = 'mCUBPFKnQf'
server = 'VitalMarkets-Live'

# # Login into mt5
if not b.mt5_login(usr, password, server):
    quit()
# b.oanda_login()
b.thread_tick_reader()
b.thread_slope_abs_rel()
b.thread_MACD()
b.thread_RSI()
# b.thread_SMAC()
# b.thread_MOMENTUM()
b.thread_orders()
b.wait()

# Making a graph of the data
# second_list = b.get_ticks()
# xAxis = []
# yAxis = []
# i = 1
# if len(second_list) < 10000:
#     for element in b.get_ticks():
#         xAxis.append(i)
#         yAxis.append(element)
#         i += 1
#
# plt.plot(xAxis, yAxis)
# plt.show()


if __name__ == '__main__':
    pass

