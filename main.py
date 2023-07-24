import json
import time
import numpy as np
import logging
from constants import *
from mt5_connector import connect_to_mt5
from main_cointegration import find_cointegrated_pairs
from mt5_data import get_time

logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    last_candle_time = 0
    while True:
        if last_candle_time != get_time('EURUSD', 5):
            try:
                # Get the current time
                last_candle_time = get_time('EURUSD', 5)

                logging.info("Storing cointegrated pairs...")
                cointegrated_pairs = find_cointegrated_pairs()

            except Exception as e:
                logging.error(f"Unexpected error occurred: {str(e)}")
                time.sleep(5)  # wait for 5 seconds before next iteration

        if True:
            #Manage Existing Positions
            pass

        if True:
            #Manage New Positions
            
