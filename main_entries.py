from constants import *
from mt5_connector import connect_to_mt5
from statistical_functions import ForexStats
from mt5_data import get_data, get_spread

import json
import logging

# Initialize logger
logger = logging.getLogger(__name__)

try:
    with open(COINTEGRATED_PAIRS_FILE, 'r') as file:
        pairs = json.load(file)
except FileNotFoundError:
    logger.error(f"Error: The file {COINTEGRATED_PAIRS_FILE} does not exist.")
    pairs = []
except json.JSONDecodeError:
    logger.error(f"Error: The file {COINTEGRATED_PAIRS_FILE} does not contain valid JSON.")
    pairs = []

for pair in pairs:
    logger.info(f'Processing pair: {pair}')
