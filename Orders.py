import logging

import MetaTrader5 as mt5
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('logs\\bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

CANDLES_BETWEEN_OPERATIONS = 3
STOPLOSS = 15000
TAKEPROFIT = 15000


def open_position(market: str, lotage: float, type_op):
    """Function to open a position.
    Args:
        market (string)
        lotage (float)
        type_op: Type of the operation
    """
    logger.info(f'''Opening positions:
    Market: {market}
    Lotage: {lotage}
    Order Type: {type_op}
''')
    point = mt5.symbol_info(market).point
    price = mt5.symbol_info_tick(market).ask

    if type_op == mt5.ORDER_TYPE_BUY:
        sl = price - STOPLOSS * point
        tp = price + TAKEPROFIT * point
    else:
        sl = price + STOPLOSS * point
        tp = price - TAKEPROFIT * point

    deviation = 20
    operation = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": market,
        "volume": lotage,
        "type": type_op,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # Sending the buy
    result = mt5.order_send(operation)
    print(
        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(market, lotage, price,
                                                                                                 deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("[Thread - orders] Failed operation: retcode={}".format(result.retcode))
        return None


def thread_orders(stop_event, data, trading_data):
    """Function executed by a thread. It checks if the conditions to open orders
    are okay.
    Args:
        stop_event (thread.Event): Event to stop the thread.
        data (dict): Dictionary with candles and the indicator.
        trading_data (dict): Dictionary with the lotage and the market.
    """
    last_operation_time = 0
    ep = datetime.datetime(1970, 1, 1, 0, 0, 0)

    while data["0"] is None and data["1"] is None:
        pass

    print("[INFO]\tOrders running")

    while not stop_event.is_set():
        cur_time = int((datetime.datetime.utcnow() - ep).total_seconds())

        if data["1"][0] < data["1"][1] \
                and cur_time > last_operation_time + trading_data[
            "time_period"] * CANDLES_BETWEEN_OPERATIONS:  # Open sell
            last_operation_time = cur_time
            open_position(trading_data["market"], trading_data["lotage"], mt5.ORDER_TYPE_SELL)