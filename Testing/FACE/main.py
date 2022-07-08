# FACE (Forex Automated Currency Exchange) Project
# V 1.0
# 6/1/2022

import logging

import bot
import keyboard
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('../logs/face/main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

b = bot.Bot(0.01, 10, "XAUUSD")

with open("login_data.txt", 'r') as f:
    lines = f.readlines()
    usr = int(lines[0])
    password = lines[1]
print('''Which server would you like to connect to?
     1: MetaQuotes-Demo''')
server = None
while server is None:
    if keyboard.is_pressed('1'):
        server = 'MetaQuotes-Demo'
        print(f'\nYou selected: {server}\n')

# Login into mt5
if not b.mt5_login(usr, password, server):
    quit()
b.thread_tick_reader()
b.thread_slope_abs_rel()
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
