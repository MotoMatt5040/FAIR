import MACD, RSI, time
import datetime as date
import MetaTrader5 as mt5
import keyboard

# Global variables
THRESHOLD = 1
MARGIN = 20
TP_MARGIN = 1
# TODO ADJUST TIME BETWEEN OPERATIONS
# TIME_BETWEEN_OPERATIONS = 5 * 60 * 10
TIME_BETWEEN_OPERATIONS = 60
STOPLOSS = 15000
TAKEPROFIT = 15000
TRAIL_AMOUNT = 50  # 50 pips


def handle_stoploss(order: int, position):
    # ticket = position.ticket
    # symbol = position.symbol
    # order_type = position.type
    # price_current = position.price_current
    # price_open = position.price_open
    # sl = position.sl
    # # calculating distance from sl
    # dist_from_sl = abs(round(price_current - sl, 6))
    #
    # # calculating new sl
    # if dist_from_sl > TRAIL_AMOUNT:
    #     if sl != 0.0:
    #         if order_type == 0:  # BUY
    #             sl = sl + TRAIL_AMOUNT
    #         elif order_type == 1:  # SELL
    #             sl = sl - TRAIL_AMOUNT
    #     request = {
    #         "action": mt5.TRADE_ACTION_SLTP,
    #         "sl": sl,
    #         # "tp": 20,
    #         "position": ticket
    #     }
    #
    #     result = mt5.order_send(request)
    #
    # else:
    #     sl = price_open - TRAIL_AMOUNT if order_type == 0 else price_open + TRAIL_AMOUNT
    #     return
    # return result
    pass

def handle_buy(buy, market):
    """Function to handle a buy operation.

    Args:
        buy : Buy operation.
        market (str): Market where the operation was openned.
    """

    position = mt5.positions_get(symbol=market)[-1].ticket
    point = mt5.symbol_info(market).point
    GOAL = buy['price'] + point * THRESHOLD
    tp = buy['price'] + TAKEPROFIT * point
    print(buy['price'])
    print(tp)
    print(point)
    moves = 0
    margin_adjustment = 0
    while True:
        tick = mt5.symbol_info_tick(market)
        if tick.ask >= GOAL:
            # Modifying the stop loss
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": market,
                "sl": tick.ask - (MARGIN - margin_adjustment) * point,
                "tp": tp,
                "deviation": 20,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                "position": position
            }
            GOAL = tick.ask + 1 * point
            # print(tick.ask - (MARGIN - margin_adjustment) * point)
            move = True
            if move:
                if margin_adjustment < 380:
                    margin_adjustment += 1
                # elif margin_adjustment <= 70:
                #     margin_adjustment = MARGIN - 70
                # elif margin_adjustment <= 80:
                #     margin_adjustment = MARGIN - 40
                # elif margin_adjustment > 80:
                #     margin_adjustment = MARGIN - 20
                # print(MARGIN - margin_adjustment)
                move = False
            # mt5.order_send(request)
        # print(tick.ask * point)

        # print(f'position: {mt5.positions_get(ticket=position)}')
        # We check if the operation has been closed in order to leave the function
        if len(mt5.positions_get(ticket=position)) == 0:
            return
        else:
            # handle_stoploss(1, mt5.positions_get(ticket=position)[0])
            pass
        time.sleep(0.1)


def handle_sell(sell, market: str):
    """Function to handle a sell operation.

    Args:
        sell : Sell operation.
        market (str): Market where the operation was opened.
    """
    position = mt5.positions_get(symbol=market)[-1].ticket
    point = mt5.symbol_info(market).point
    GOAL = sell['price'] - point * THRESHOLD
    tp = sell['price'] - TAKEPROFIT * point
    print(sell['price'])
    print(tp)
    margin_adjustment = 0
    moves = 0
    while True:
        tick = mt5.symbol_info_tick(market)
        if tick.bid <= GOAL:
            # Modifying the stop loss
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": market,
                "sl": tick.bid + (MARGIN - margin_adjustment) * point,
                "tp": tp,
                "deviation": 20,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
                "position": position
            }
            GOAL = tick.bid - 1 * point
            # print(tick.ask - (MARGIN - margin_adjustment) * point)
            move = True
            if move:
                if margin_adjustment < 380:
                    margin_adjustment += 1
                # elif margin_adjustment <= 70:
                #     margin_adjustment = MARGIN - 70
                # elif margin_adjustment <= 80:
                #     margin_adjustment = MARGIN - 40
                # elif margin_adjustment > 80:
                #     margin_adjustment = MARGIN - 20
                # print(MARGIN - margin_adjustment)
                move = False
            # mt5.order_send(request)
        # print(tick.ask * point)

        # print(f'position: {mt5.positions_get(ticket=position)}')
        # We check if the operation has been closed in order to leave the function
        if len(mt5.positions_get(ticket=position)) == 0:
            return
        else:
            pass
            # handle_stoploss(1, mt5.positions_get(ticket=position)[0])
        time.sleep(0.1)


def open_buy(trading_data: dict):
    """Function to open a buy operation.

    Args:
        trading_data (dict): Dictionary with all the needed data.

    Returns:
        A buy.
    """
    symbol_info = mt5.symbol_info(trading_data['market'])
    if symbol_info is None:
        print("[Thread - orders]", trading_data['market'], "not found, can not call order_check()")
        return None

    counter = 0
    # We only open the operation if the spread is 0
    # we check the spread 300000 times
    while symbol_info.spread > 220 and counter < 300000:
        counter += 1
        symbol_info = mt5.symbol_info(trading_data['market'])

    # If the spread wasn't 0 then we do not open the operation
    if counter == 300000:
        now = date.datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        print("[Thread - orders]", dt_string, "- Spread too high. Spread =", symbol_info.spread)
        return None

    # If the symbol is not available in the MarketWatch, we add it
    if not symbol_info.visible:
        print("[Thread - orders]", trading_data['market'], "is not visible, trying to switch on")
        if not mt5.symbol_select(trading_data['market'], True):
            print("[Thread - orders] symbol_select({}) failed, exit", trading_data['market'])
            return None

    point = mt5.symbol_info(trading_data['market']).point
    price = mt5.symbol_info_tick(trading_data['market']).ask
    deviation = 20
    buy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": trading_data['market'],
        "volume": trading_data['lotage'],
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - STOPLOSS * point,
        "tp": price + TAKEPROFIT * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the buy
    result = mt5.order_send(buy)
    print(
        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(trading_data['market'],
                                                                                                 trading_data['lotage'],
                                                                                                 price, deviation))
    try:
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("[Thread - orders] Failed buy: retcode={}".format(result.retcode))
            return None
    except Exception as err:
        print(err)
    return buy


def open_sell(trading_data: dict):
    """Function to open a sell operation.

    Args:
        trading_data (dict): Dictionary with all the needed data.

    Returns:
        A sell.
    """
    symbol_info = mt5.symbol_info(trading_data['market'])
    if symbol_info is None:
        print("[Thread - orders]", trading_data['market'], "not found, can not call order_check()")
        return None

    counter = 0
    # We only open the operation if the spread is 0
    # we check the spread 300000 times
    while symbol_info.spread > 220 and counter < 300000:
        counter += 1
        symbol_info = mt5.symbol_info(trading_data['market'])

    # If the spread wasn't 0 then we do not open the operation
    if counter == 300000:
        now = date.datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        print("[Thread - orders]", dt_string, "- Spread too high. Spread =", symbol_info.spread)
        return None

    # if the symbol is not available in MarketWatch, we add it
    if not symbol_info.visible:
        print("[Thread - orders]", trading_data['market'], "is not visible, trying to switch on")
        if not mt5.symbol_select(trading_data['market'], True):
            print("[Thread - orders] symbol_select({}) failed, exit", trading_data['market'])
            return None

    point = mt5.symbol_info(trading_data['market']).point
    price = mt5.symbol_info_tick(trading_data['market']).bid
    deviation = 20
    sell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": trading_data['market'],
        "volume": trading_data['lotage'],
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + STOPLOSS * point,
        "tp": price - TAKEPROFIT * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the sell
    result = mt5.order_send(sell)
    print(
        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(trading_data['market'],
                                                                                                 trading_data['lotage'],
                                                                                                 price, deviation))
    try:
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("[Thread - orders] failed sell: {}".format(result.retcode))
            return None
    except Exception as err:
        print(err)
    return sell


def check_buy() -> bool:
    """Function to check if we can open a buy.

    Returns:
        bool: True if we can, false if not.
    """
    # TODO REMOVE PRINT LINES
    # print(MACD.check_buy(), RSI.check_buy())
    return MACD.check_buy() and RSI.check_buy()
    # TODO FIX RETURN STATEMENT
    # return True
    # return SMACrossover.check_buy()

def check_sell() -> bool:
    """Function to check if we can open a sell.

    Returns:
        bool: True if we can, false if not.
    """
    # TODO FIX RETURN STATEMENT
    return MACD.check_sell() and RSI.check_sell()
    # return True
    # return SMACrossover.check_sell()

def thread_orders(pill2kill, trading_data: dict):
    """Function executed by a thread. It opens and handles operations.

    Args:
        pill2kill (Threading.Event): Event to stop the thread's execution.
        trading_data (dict): Dictionary with all the needed data
        for opening operations.
    """
    print("[THREAD - orders] - Working")

    last_operation = 0
    print("[THREAD - orders] - Checking operations\n")
    initialized = False
#
#     print("""Buy: 1
# Sell: 2""")
#
    # order = None
    # while order is None:
    #     if keyboard.is_pressed('1'):
    #         order = 1
    #     elif keyboard.is_pressed('2'):
    #         order = 2


    # if not initialized:
    #     for i in range(2):
    #         time.sleep(.1)
    #         # if order == 1:
    #         buy = open_buy(trading_data)
    #         # elif order == 2:
    #         #     sell = open_sell(trading_data)
    #     initialized = True

    # TODO Verrify that buy/sell operation is working properly.

    while not pill2kill.wait(0.1):
        # TODO REMOVE PRINT STATEMENT
        # print(check_buy(), check_sell(), last_operation, TIME_BETWEEN_OPERATIONS)
        order = 2
        if check_buy() and last_operation > TIME_BETWEEN_OPERATIONS:
            buy = open_buy(trading_data)
            last_operation = 0
            if buy is not None:
                order = 0
                now = date.datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                print("[Thread - orders] Buy open -", dt_string)
                handle_buy(buy, trading_data['market'])
                buy = None

        if check_sell() and last_operation > TIME_BETWEEN_OPERATIONS:
            sell = open_sell(trading_data)
            last_operation = 0
            if sell is not None:
                order = 2
                now = date.datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                print("[Thread - orders] Sell open -", dt_string)
                handle_sell(sell, trading_data['market'])
                sell = None

        last_operation += 1