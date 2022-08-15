# Global variables
MACDs = []
PREV_MACD = None
PREV_SIGNAL = None
CUR_MACD = None
CUR_SIGNAL = None

PREV_EMA9 = None
PREV_EMA12 = None
PREV_EMA26 = None

ema_fast = 12
ema_slow = 26
# smooth = 5

MAX_LEN = 9  # 9

# TODO MAX_LEN = 9, ema_fast = 12, ema_slow = 26


def check_buy() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation.

    Returns:
        bool: True if it is a buy opportunity, false if not
    """
    # TODO REMOVE PRINT LINE
    # print(f'Previous MACD: {PREV_MACD}|Previous Signal: {PREV_SIGNAL}||Current MACD: {CUR_MACD}|Current Signal: {CUR_SIGNAL}')
    if CUR_SIGNAL == None or CUR_MACD == None \
            or PREV_SIGNAL == None or PREV_MACD == None:
        return False
    if PREV_SIGNAL >= PREV_MACD:
        if CUR_SIGNAL <= CUR_MACD:
            return True
    return False


def check_sell() -> bool:
    """Function to check if the MACD indicator
    allows a buy operation.

    Returns:
        bool: True if it is a buy opportunity, false if not
    """

    if CUR_SIGNAL == None or CUR_MACD == None \
            or PREV_SIGNAL == None or PREV_MACD == None:
        return False
    if PREV_SIGNAL <= PREV_MACD:
        if CUR_SIGNAL >= CUR_MACD:
            return True
    return False


def K(n):
    """Function for calculating k

    Args:
        n (int): Length

    Returns:
        float: value
    """
    return 2 / (n + 1)


def SMA(ticks):
    """Function that computes the Simple Moving Average.

    Args:
        ticks (list): List with prices.

    Returns:
        float: value
    """
    return sum(ticks) / len(ticks)


def EMA(ticks: list, n: int):
    """Function that computes the Exponential Moving Average.

    Args:
        ticks (list): List of prices.
        n (int): Number of values to take into account.
        n can only be 12, 9 or 26.

    Returns:
        float: Value of the EMA
    """
    global PREV_EMA12, PREV_EMA26, PREV_EMA9

    # if n != 12 and n != 26 and n != 9:
    if n != ema_fast and n != ema_slow and n != MAX_LEN:
        print(f"EMA function: N must be {ema_fast} or {ema_slow} or {MAX_LEN}")

    # Not enough ticks in the list
    if n > len(ticks): return None

    k = K(n)

    # Checking if the previous EMA has been calculated
    prev_ema = 0
    if n == ema_fast:
        if PREV_EMA12 is None:
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA12
        ema = (ticks[-1] - prev_ema) * k + prev_ema
        PREV_EMA12 = ema
    elif n == ema_slow:
        if PREV_EMA26 is None:
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA26
        ema = (ticks[-1] - prev_ema) * k + prev_ema
        PREV_EMA26 = ema
    else:
        if PREV_EMA9 is None:
            prev_ema = SMA(ticks)
        else:
            prev_ema = PREV_EMA9
        ema = (ticks[-1] - prev_ema) * k + prev_ema
        PREV_EMA9 = ema

    return ema


def MACD(ticks):
    """Function that computes the MACD.

    Args:
        ticks (list): List with prices of the ticks

    Returns:
        float: Value of the MACD.
    """
    return EMA(ticks[-ema_fast:], ema_fast) - EMA(ticks[-ema_slow:], ema_slow)


def SIGNAL(values_list):
    """Function that computes the SIGNAL.

    Args:
        values_list (list): List with which we have to compute the values.

    Returns:
        float: Value of the SIGNAL.
    """
    return EMA(values_list[-MAX_LEN:], MAX_LEN)


def thread_macd(pill2kill, ticks: list, indicators: dict, trading_data: dict):
    """Function executed by a thread that calculates
    the MACD and the SIGNAL.

    Args:
        pill2kill (Threading.Event): Event for stopping the thread's execution.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the data is going to be stored.
        trading_data (dict): Dictionary where the data about our bot is stored.
    """
    global MACDs, CUR_SIGNAL, CUR_MACD, PREV_SIGNAL, PREV_MACD

    # Wait if there are not enough elements
    while len(ticks) < 35 and not pill2kill.wait(1.5):
        print("[THREAD - MACD] - Waiting for ticks\n")

    print("[THREAD - MACD] - Loading values")
    # First we need to calculate the previous MACDs and SIGNALs
    i = ema_slow
    while i < len(ticks):
        # Computing the MACD
        PREV_MACD = CUR_MACD
        CUR_MACD = MACD(ticks[:i])
        MACDs.append(CUR_MACD)

        i += 1

        # Computing the SIGNAL
        if len(MACDs) < MAX_LEN:
            continue
        else:
            PREV_SIGNAL = CUR_SIGNAL
            CUR_SIGNAL = SIGNAL(MACDs)

        if len(MACDs) > MAX_LEN:
            del MACDs[0]

    # Main thread loop
    print("[THREAD - MACD] - Computing values")
    i = 0
    while not pill2kill.wait(1):
        # Computing the MACD
        PREV_MACD = CUR_MACD
        CUR_MACD = MACD(ticks[-ema_slow:])

        # Only append a MACD value every time period
        if i >= trading_data['time_period']:
            MACDs.append(CUR_MACD)
            i = 0
        else:
            MACDs[-1] = CUR_MACD
        i += 1

        # Computing the SIGNAL
        PREV_SIGNAL = CUR_SIGNAL
        CUR_SIGNAL = SIGNAL(MACDs)

        # Updating the dictionary
        indicators['MACD']['MACD'] = CUR_MACD
        indicators['MACD']['SIGNAL'] = CUR_SIGNAL
        # TODO REMOVE PRINT LINE
        # print(PREV_MACD, PREV_SIGNAL, CUR_MACD, CUR_SIGNAL)

        if len(MACDs) > MAX_LEN:
            del MACDs[0]
