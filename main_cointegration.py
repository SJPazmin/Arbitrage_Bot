import json
import numpy as np
import os
import logging
from statistical_functions import ForexStats
from mt5_data import get_data
from constants import *

# Initialize logger
logger = logging.getLogger(__name__)


def find_cointegrated_pairs():
    # Attempt to load JSON file containing currency pairs to check
    try:
        with open(PAIRS_CORR_FILE, 'r') as file:
            pairs = json.load(file)
    # Handle file not found error
    except FileNotFoundError:
        logger.error(f"Error: The file {PAIRS_CORR_FILE} does not exist.")
        return []
    # Handle invalid JSON error
    except json.JSONDecodeError:
        logger.error(
            f"Error: The file {PAIRS_CORR_FILE} does not contain valid JSON.")
        return []

    # Initialize list to store cointegrated pairs
    cointegrated_pairs = []

    # Iterate over each pair
    for pair in pairs:
        logger.info(f'Processing pair: {pair}')

        # Get data for the given pair
        data = get_data(pair, 5, WINDOW_LENGTH, 'close', 'dataframe')

        # Split data into two arrays for analysis
        arr1 = np.array(data.iloc[:, 0])
        arr2 = np.array(data.iloc[:, 1])

        # Initialize ForexStats class with the two time series
        forex_stats = ForexStats(arr1, arr2)

        # If pair is highly correlated, cointegrated, and has a half-life less than or equal to 35
        if forex_stats.calculate_correlation() > 0.7 and forex_stats.check_cointegration() and forex_stats.calculate_half_life() <= 35:
            # Add to the list of cointegrated pairs
            cointegrated_pairs.append(pair)

    # Save cointegrated pairs to JSON file for later use
    with open(COINTEGRATED_PAIRS_FILE, 'w') as file:
        json.dump(cointegrated_pairs, file, indent=4)

    return cointegrated_pairs
