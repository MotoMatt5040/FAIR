# FAIR (Forex AI Repository) Project
# V 1.0
# 5/10/2022

import logging
import MetaTrader5 as mt5
from bot import Bot

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

login = False
usr = None
password = None

while usr is None:
    try:
        usr = int(input('Username: '))
    except:
        print('Incorrect user.')
password = input('Password: ')

logger.info('Opening/Initializing MT5 Connection')
LOGIN = 5003534489
PASSWORD = '6jsxifbk'
mt5.initialize(login=usr, password=password, server='MetaQuotes-Demo')
print(mt5.account_info())


macd_bot = Bot(lotage=0.1, time_period=60, market="Boom 300 Index")

macd_bot.start()
macd_bot.wait()


if __name__ == '__main__':
    pass

