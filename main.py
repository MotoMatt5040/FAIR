# FAIR (Forex AI Repository) Project
# V 1.0
# 5/10/2022

import logging

import pandas as pd
import MetaTrader5 as mt5
from bot import Bot
import keyboard

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

usr = None
password = None
server = None

while usr is None:
    try:
        usr = int(input('Username: '))
    except:
        print('Incorrect user.')
password = input('Password: ')
print('''Which server would you like to connect to?
    1: MetaQuotes-Demo''')
while server is None:
    if keyboard.is_pressed('1'):
        server = 'MetaQuotes-Demo'
        print(f'\nYou selected: {server}\n')

logger.info('Opening/Initializing MT5 Connection')
usr = 5003534489
password = '6jsxifbk'
if mt5.initialize(login=usr, password=password, server='MetaQuotes-Demo'):
    print(f'Connection to MetaTrader5 server successful.')
    print()
    account_info = mt5.account_info()
    if account_info is not None:
        account_info_dict = mt5.account_info()._asdict()
        print('*****Account Info*****\n')
        for item in account_info_dict:
            print(f"{item}: {account_info_dict[item]}")
        print()
        print()
    terminal_info = mt5.terminal_info()
    if terminal_info is not None:
        print('*****Terminal Info*****\n')
        terminal_info_dict = mt5.terminal_info()._asdict()
        for item in terminal_info_dict:
            print(f"{item}: {terminal_info_dict[item]}")
        print()
        print()
else:
    quit(f'''Connection to MetaTrader5 server unsuccessful!
    Error: {mt5.last_error()}
    
    Please restart the program.
''')

macd_bot = Bot(lotage=0.1, time_period=60, market="Boom 300 Index")

macd_bot.start()
macd_bot.wait()


if __name__ == '__main__':
    pass

