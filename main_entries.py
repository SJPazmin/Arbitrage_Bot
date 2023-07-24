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
# Handle file not found error
except:
    pairs = []

for pair in pairs:
    print(f'Processing pair: {pair}')
