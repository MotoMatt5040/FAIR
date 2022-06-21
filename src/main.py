# FAIR (Forex AI Repository) Project
# V 1.0
# 5/10/2022

import logging

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
b = bot.Bot(1.5, 10, "XAUUSD")

with open("login_data.txt", 'r') as f:
    lines = f.readlines()
    usr = int(lines[0])
    password = lines[1]


# Login into mt5
if not b.mt5_login(usr, password):
    quit()
b.thread_tick_reader()
b.thread_slope_abs_rel()
b.thread_MACD()
b.thread_RSI()
b.thread_orders()
b.wait()

# Making a graph of the data
second_list = b.get_ticks()
xAxis = []
yAxis = []
i = 1
if len(second_list) < 10000:
    for element in b.get_ticks():
        xAxis.append(i)
        yAxis.append(element)
        i += 1

plt.plot(xAxis, yAxis)
plt.show()


if __name__ == '__main__':
    pass

