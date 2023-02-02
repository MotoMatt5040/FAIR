# FAIR (Forex AI Repository) Project
# V 2.0
# 5/10/2022

import logging
import time

import keyboard

import bot

# Creating a bot
# TODO Fix bot statement
b = bot.Bot(0.1, 60, "US30")
# b = bot.Bot(5.0, 60 * 15, "USDJPY!")

#dakota
# usr = 10024165
# password = 'mCUBPFKnQf'

#matt
# usr = 10024028
# password = 'qMnkbKzXHG'
#
# server = 'VitalMarkets-Live'

usr = 185201
password = 'bpfnyNVumH'
server = 'VitalMarkets-Demo'


# # Login into mt5
if not b.mt5_login(usr, password, server):
    quit()
b.thread_tick_reader()
b.thread_slope_abs_rel()
b.thread_MACD()
b.thread_RSI()
b.thread_orders()
b.wait()


if __name__ == '__main__':
    pass

