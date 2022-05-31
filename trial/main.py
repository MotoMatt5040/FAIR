# FAIR (Forex AI Repository) Project
# V 1.1
# 5/26/2022

import logging
import keyboard
import bot

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('../logs/trial/main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

b = bot.Bot(0.01, 10, "XAUUSD")

with open("login_info.txt", 'r') as f:
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