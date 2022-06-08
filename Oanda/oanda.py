import pandas as pd
import tpqoa

api = tpqoa.tpqoa("oanda.cfg")

# summary = api.get_account_summary()
# for item in summary:
#     print(f'{item}: {summary[item]}')
# # print(api.get_account_summary().keys())
# print(api.account_type)
# print(api.account_id)
# instruments = api.get_instruments()
# for item in instruments:
#     print(item)
# instr = api.get_instruments()
# print(len(instr))
# print(instr[0])

# help(api.get_history)
#
# df = api.get_history(instrument = "EUR_USD", start = "2022-05-01", end = "2022-05-31",
#                 granularity = "D", price = "B")

# df.info()
# print(df.to_string())

# api.stream_data('EUR_USD', stop=10)
# api.stop_stream()

# api.create_order(instrument='EUR_USD', units=100000, sl_distance=0.1)
# summary = api.get_account_summary()
# transaction = api.get_transactions()
# api.print_transactions()
# for item in summary:
#     print(f'{item}: {summary[item]}')


# api.create_order(instrument='EUR_USD', units=-100000, sl_distance=0.1)
# summary = api.get_account_summary()
# transaction = api.get_transactions()
# api.print_transactions()
# for item in summary:
#     print(f'{item}: {summary[item]}')