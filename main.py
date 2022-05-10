# FAIR (Forex AI Repository) Project
# V 1.0
# 5/10/2022

import logging
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(levelName)s:%(message)s')
file_handler = logging.FileHandler('logs\main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propegate = False

if __name__ == '__main__':
    pass