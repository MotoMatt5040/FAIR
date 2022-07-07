import tpqoa
import pandas as pd


class CloneClass(tpqoa.tpqoa):

    def on_success(self, time, bid, ask):
        print(f"Time: {time} | Bid: {bid} | Ask:{ask}")
