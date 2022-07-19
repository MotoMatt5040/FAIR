import time
import SMACBacktester as smacb
import pickle

sma_updater = None

smas = None
smal = None
smas_value = None
smal_value = None


def check_buy() -> bool:
    """Function to check if the SMACrossover allows
    a buy operation.

    Returns:
        bool: True if SMACrossover allows, false if not.
    """
    if smal_value == None or smas_value == None:
        return False

    if smal_value > smas_value:
        # print(f"Don't buy: {smal_value} > {smas_value}")
        return False
    elif smas_value > smal_value:
        # print(f"Buy: {smas_value} > {smal_value}")
        return True
    return False


def check_sell() -> bool:
    """Function to check if the SMACrossover
    allows a sell operation.

    Returns:
        bool: True if SMACrossover allows, false if not.
    """
    if smal_value == None or smas_value == None:
        return False

    if smal_value < smas_value:
        # print(f"Don't sell: {smal_value} < {smas_value}")
        return False
    elif smas_value < smal_value:
        # print(f"Sell: {smas_value} < {smal_value}")
        return True
    return False


def SMAL(ticks):
    """Function that computes the Long Simple Moving Average.

    Args:
        ticks (list): List with prices.

    Returns:
        float: value
    """
    smal = sma_updater[1]
    return sum(ticks[:smal]) / smal


def SMAS(ticks):
    """Function that computes the Short Simple Moving Average.

    Args:
        ticks (list): List with prices.

    Returns:
        float: value
    """
    smas = sma_updater[0]
    return sum(ticks[:smas]) / smas


def thread_SMAC(pill2kill, ticks: list, indicators: dict):
    """Function executed by a thread. Calculates the SMA Short/Long and
    stores it in the dictionary.

    Args:
        pill2kill (Threading.event): Event for stopping the threads executuion.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the values are stored.
    """

    global smas, smal, sma_updater, smas_value, smal_value

    # Wait if there are not enough elements
    while len(ticks) < 100 and not pill2kill.wait(1.5):
        print("[THREAD - SMAC] - Waiting for ticks\n")

    print("[THREAD - SMAC] - Computing values\n")
    tester = smacb.SMACBacktester(ticks=ticks)
    print(tester.optimize_parameters((1, 20, 1), (21, 100, 1)))
    sma_updater = pickle.load(open("sma_update.pkl", "rb"))
    smas = sma_updater[0]
    smal = sma_updater[1]

    while not pill2kill.wait(1):
        smas_value = SMAS(ticks[::-1])
        smal_value = SMAL(ticks[::-1])
        indicators['SMAC']['SMAS'] = smas_value
        indicators['SMAC']['SMAL'] = smal_value


def thread_SMAC_update(pill2kill, ticks: list, indicators: dict):
    """Function executed by a thread. Calculates the SMA Short/Long and
    stores it in the dictionary.

    Args:
        pill2kill (Threading.event): Event for stopping the threads executuion.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the values are stored.
    """

    global smas, smal, sma_updater, smas_value, smal_value

    # Wait if there are not enough elements
    while len(ticks) < 100 and not pill2kill.wait(1.5):
        print("[THREAD - SMAC] - Waiting for ticks\n")

    print("[THREAD - SMAC] - Computing values\n")
    tester = smacb.SMACBacktester(ticks=ticks)


    while not pill2kill.wait(900):
        print(tester.optimize_parameters((1, 20, 1), (21, 100, 1)))
        sma_updater = pickle.load(open("sma_update.pkl", "rb"))
        smas = sma_updater[0]
        smal = sma_updater[1]
        smas_value = SMAS(ticks[::-1])
        smal_value = SMAL(ticks[::-1])
        indicators['SMAC']['SMAS'] = smas_value
        indicators['SMAC']['SMAL'] = smal_value

