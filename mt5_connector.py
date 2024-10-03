import MetaTrader5 as mt5
import logging
import time

logging.basicConfig(level=logging.INFO)


def connect_to_mt5(retries=3, delay=1):
    """
    Connects to a MetaTrader5 account.

    Args:
        retries (int): The number of times to retry the connection attempt.
        delay (int): The time delay (in seconds) between connection attempts.

    Returns:
        bool: True if the connection was successful, False otherwise.
    """

    # Attempt to connect to the MetaTrader5 account
    for i in range(retries):
        try:
            if mt5.initialize():
                logging.info('Connected to MetaTrader5 account.')
                return True
            else:
                logging.error('Failed to initialize MetaTrader5.')
        except Exception as e:
            logging.error(f'Failed to connect to MetaTrader5: {e}')

        # Wait before the next attempt
        time.sleep(delay)

    logging.error('Failed to connect to MetaTrader5 after retries.')
    return False


if __name__ == "__main__":
    connect_to_mt5()
