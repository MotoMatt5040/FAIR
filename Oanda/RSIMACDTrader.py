import pandas as pd
import numpy as np
import tpqoa
from datetime import datetime, timedelta
import time


class SMACTrader(tpqoa.tpqoa):

    def __init__(self, config_file, instrument, bar_length, rsi, macdsp, macdlp, macds, units):
        super().__init__(config_file)
        self.instrument = instrument  # define instrument
        self.bar_length = pd.to_timedelta(bar_length)  # Pandas Timedelta Object
        self.tick_data = pd.DataFrame()
        self.raw_data = None
        self.data = None
        self.last_bar = None
        self.units = units
        self.position = 0
        self.profits = []

        # *****************add strategy-specific attributes here******************
        self.rsi = rsi
        self.macdsp = macdsp
        self.macdlp = macdlp
        self.macds = macds
        # ************************************************************************

    def get_most_recent(self, days=5):
        while True:
            time.sleep(2)
            now = datetime.utcnow()
            now = now - timedelta(microseconds=now.microsecond)
            past = now - timedelta(days=days)
            df = self.get_history(instrument=self.instrument, start=past, end=now,
                                  granularity="S5", price="M", localize=False).c.dropna().to_frame()
            df.rename(columns={"c": self.instrument}, inplace=True)
            df = df.resample(self.bar_length, label="right").last().dropna().iloc[:-1]
            self.raw_data = df.copy()  # first defined
            self.last_bar = self.raw_data.index[-1]  # first defined

            # accept, if less than [bar_length] has elapsed since the last full historical bar and now
            if pd.to_datetime(datetime.utcnow()).tz_localize("UTC") - self.last_bar < self.bar_length:
                break

    def on_success(self, time, bid, ask):
        print(self.ticks, end=" ", flush=True)  # Print running Tick number

        # collect and store tick data
        recent_tick = pd.to_datetime(time)  # Pandas Timestamp Object
        # print(recent_tick, pd.to_datetime('8:05').time())

        if recent_tick.time() <= pd.to_datetime('11:05').time() and recent_tick.time() >= pd.to_datetime('21:55').time():
            print(recent_tick, pd.to_datetime('8:00').time())
            self.stop_stream = True
            time.sleep(300)


        df = pd.DataFrame({self.instrument: (ask + bid) / 2},
                          index=[pd.to_datetime(time)])  # mid price only
        # self.tick_data = self.tick_data.append(df)  # old method to append is not supported, use concat
        self.tick_data = pd.concat([self.tick_data, df])  # new method to append to df

        # if a time longer than the bar_length has elapsed between last full bar and the most recent tick
        if recent_tick - self.last_bar > self.bar_length:
            self.resample_and_join()
            self.define_strategy()  # Prepare Data / Strategy Features
            self.execute_trades()

    def resample_and_join(self):
        # self.data = self.tick_data.resample(self.bar_length, label = "right").last().ffill().iloc[:-1]
        #append the most recent ticks (resampled) to self.data
        # self.data = self.data.append(self.tick_data.resample(self.bar_length, label="right").last().ffill().iloc[:-1])
        self.raw_data = pd.concat([self.raw_data, self.tick_data.resample(
            self.bar_length, label="right").last().ffill().iloc[:-1]])
        self.tick_data = self.tick_data.iloc[-1:]  # only keep the latest tick (next bar)
        self.last_bar = self.raw_data.index[-1]

    def define_strategy(self):  # "strategy-specific"
        df = self.raw_data.copy()  # self.raw_data new!

        # ******************** define your strategy here ************************
        # TODO Add in calculation for peaks inside of crossovers to maximize profits from volatility.
        # one method could be to check price of tick and every time the current price is below the previous price
        # you reset the lowest price. That can use a contrarian strategy with a window of 3. Close order then choose to
        # buy or sell. Most likely if we bought we would choose to sell at that point. Bollinger bands might be a
        # better option than contrarian strategy

        #SMA Crossover
        df['SMAS'] = df[self.instrument].rolling(self.smas).mean()
        df['SMAL'] = df[self.instrument].rolling(self.smal).mean()
        df['sposition'] = np.where(df['SMAS'] > df['SMAL'], 1, -1)

        #Bollinger
        df["SMA"] = df[self.instrument].rolling(self.sma).mean()
        df["Lower"] = df["SMA"] - df[self.instrument].rolling(self.sma).std() * self.dev
        df["Upper"] = df["SMA"] + df[self.instrument].rolling(self.sma).std() * self.dev
        df["distance"] = df[self.instrument] - df.MSMA
        df["bposition"] = np.where(df[self.instrument] < df.Lower, 1, np.nan)
        df["bposition"] = np.where(df[self.instrument] > df.Upper, -1, df["bposition"])
        df["bposition"] = np.where(df.distance * df.distance.shift(1) < 0, 0, df["bposition"])
        df["bposition"] = df.bposition.ffill().fillna(0)

        #Define position
        df['position'] = np.where(df['sposition'] == df['bposition'], df['sposition'], 0)
        # ***********************************************************************

        self.data = df.copy()  # first defined here

    def execute_trades(self):
        if self.data["position"].iloc[-1] == 1:
            if self.position == 0:
                order = self.create_order(self.instrument, self.units, suppress=True, ret=True)
                self.report_trade(order, "GOING LONG")
            elif self.position == -1:
                order = self.create_order(self.instrument, self.units * 2, suppress=True, ret=True)
                self.report_trade(order, "GOING LONG")
            self.position = 1
        elif self.data["position"].iloc[-1] == -1:
            if self.position == 0:
                order = self.create_order(self.instrument, -self.units, suppress=True, ret=True)
                self.report_trade(order, "GOING SHORT")
            elif self.position == 1:
                order = self.create_order(self.instrument, -self.units * 2, suppress=True, ret=True)
                self.report_trade(order, "GOING SHORT")
            self.position = -1
        elif self.data["position"].iloc[-1] == 0:
            if self.position == -1:
                order = self.create_order(self.instrument, self.units, suppress=True, ret=True)
                self.report_trade(order, "GOING NEUTRAL")
            elif self.position == 1:
                order = self.create_order(self.instrument, -self.units, suppress=True, ret=True)
                self.report_trade(order, "GOING NEUTRAL")
            self.position = 0

    def report_trade(self, order, going):
        time = order["time"]
        units = order["units"]
        price = order["price"]
        pl = float(order["pl"])
        self.profits.append(pl)
        cumpl = sum(self.profits)
        print("\n" + 100 * "-")
        print("{} | {}".format(time, going))
        print("{} | units = {} | price = {} | P&L = {} | Cum P&L = {}".format(time, units, price, pl, cumpl))
        print(100 * "-" + "\n")

    #  def reset_parameters(self):

