import time


pos = [0,0,0]


def check_buy() -> bool:
    """Function to check if the Momentum allows
    a buy operation.

    Returns:
        bool: True if Momentum allows, false if not.
    """

    return False


def check_sell() -> bool:
    """Function to check if the Momentum
    allows a sell operation.

    Returns:
        bool: True if Momentum allows, false if not.
    """

    return False




def momentum(ticks):
    """Function that computes the Momentum Direction.

    Args:
        ticks (list): List with prices.

    Returns:
        float: value
    """
    global pos
    # value = ticks[-3:] / 3
    # print(value)
    # print(ticks[:3])
    # print(ticks[0], ticks[1], ticks[2], ticks[3])
    # pos[0] = ticks[0] - ticks[1]
    # pos[1] = ticks[1] - ticks[2]
    # pos[2] = ticks[2] - ticks[3]
    # print(pos)
    return 0

def thread_Momentum(pill2kill, ticks: list, indicators: dict):
    """Function executed by a thread. Calculates the Momentum and
    stores it in the dictionary.

    Args:
        pill2kill (Threading.event): Event for stopping the threads executuion.
        ticks (list): List with prices.
        indicators (dict): Dictionary where the values are stored.
    """
    # Wait if there are not enough elements
    while len(ticks) < 100 and not pill2kill.wait(1.5):
        print("[THREAD - MOMENTUM] - Waiting for ticks\n")

    print("[THREAD - MOMENTUM] - Computing values\n")


    while not pill2kill.wait(1):
        pos = momentum(ticks[::-1])
        indicators['MOMENTUM']['MOMENTUM'] = pos


