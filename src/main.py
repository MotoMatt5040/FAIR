# FAIR (Forex AI Repository) Project
# V 1.0
# 5/10/2022

import logging
import time

import keyboard

import bot
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('../logs/main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

# Creating a bot
# TODO Fix bot statement
# b = bot.Bot(0.01, 5 * 60, "XAUUSD")
b = bot.Bot(3.0, 10, "USDJPY")

markets = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']

# for market in markets:


# with open("login_data.txt", 'r') as f:
#     lines = f.readlines()
#     usr = int(lines[0])
#     password = lines[1]

print('''Which account would you like to use
    1: MT5 Demo
    2: Hanko Demo''')
usr = None
while usr is None:
    if keyboard.is_pressed('1'):
        usr = 5003534489
        password = '6jsxifbk'
        print(f'\nYou selected: {usr}\n')
    elif keyboard.is_pressed('2'):
        usr = 805062
        password = 'R6rz@i@Ue!#bCAn'
        print(f'\nYou selected: {usr}\n')

time.sleep(0.1)
print('''Which server would you like to connect to?
    1: MetaQuotes-Demo
    2: OANDA-Demo-2
    3: Hankotrade-Demo''')
server = None
while server is None:
    if keyboard.is_pressed('1'):
        server = 'MetaQuotes-Demo'
        print(f'\nYou selected: {server}\n')
    elif keyboard.is_pressed('2'):
        server = 'OANDA-Demo-2'
        print(f'\nYou selected: {server}\n')
    elif keyboard.is_pressed('3'):
        server = 'Hankotrade-Demo'
        print(f'\nYou selected: {server}\n')

# Login into mt5
if not b.mt5_login(usr, password, server):
    quit()
b.thread_tick_reader()
b.thread_slope_abs_rel()
b.thread_MACD()
b.thread_RSI()
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

