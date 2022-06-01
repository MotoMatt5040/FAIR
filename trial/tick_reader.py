import MetaTrader5 as mt5
import datetime
import pytz

# Global variables
MAX_TICKS_LEN = 200
MAX_LEN_SPREAD = 20
spread_list = []

def load_ticks(ticks: list, market: str, time_period: int):
    """Function to load into a list, previous ticks.

        Args:
            ticks (list): List where to load ticks.
            market (str): Market from which we have to take ticks.
            time_period (int): Time period in which we want to operate.
            1 minute, 15 minutes... (in seconds)
        """
    # Checking if we are on the weekend (including friday)
    # if so, we take ticks from an earlier date.

    today = datetime.datetime.utcnow().date()
    if today.weekday() >= 5 or today.weekday() == 0:
        yesterday = today - datetime.timedelta(days=3)
    else:
        yesterday = today - datetime.timedelta(days=1)

    # loading data
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.datetime(int(yesterday.year), int(yesterday.month), int(yesterday.day), tzinfo=timezone)
    loaded_ticks = mt5.copy_ticks_from(market, utc_from, 300000, mt5.COPY_TICKS_ALL)
    if loaded_ticks is None:
        print("Error loading the ticks")
        return -1

    # Filling the list
    second_to_include = loaded_ticks[0][0]
    for tick in loaded_ticks:
        # Every X seconds we add a value to the list
        if tick[0] > second_to_include + time_period:
            ticks.append(tick[2])
            second_to_include = tick[0]

    # Removing the ticks that we do not need
    not_needed_ticks = len(ticks) - MAX_TICKS_LEN
    if not_needed_ticks > 0:
        for i in range(not_needed_ticks):
            del ticks[0]

    print(loaded_ticks, ticks, not_needed_ticks)
