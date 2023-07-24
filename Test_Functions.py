from statistical_functions import ForexStats
from mt5_data import get_data
import numpy as np

# Get the data for two forex symbols
data = get_data(['EURUSD', 'GBPUSD'],
                5, 288, 'close', 'dataframe')

# Convert the close prices to numpy arrays
arr1 = np.array(data.iloc[:, 0])
arr2 = np.array(data.iloc[:, 1])

# Initialize the ForexStats class with the data
forex_stats = ForexStats(arr1, arr2)

# Now you can use the methods of the ForexStats class:
correlation = forex_stats.calculate_correlation()
print(f'Correlation: {correlation}')

is_cointegrated = forex_stats.check_cointegration()
print(f'Are the symbols cointegrated? {is_cointegrated}')

spread = forex_stats.calculate_spread()
print(f'Spread: {spread}')

half_life = forex_stats.calculate_half_life()
print(f'Half-Life of the Spread: {half_life}')

hedge_ratio = forex_stats.calculate_hedge_ratio()
print(f'Hedge Ratio: {hedge_ratio}')

z_score = forex_stats.calculate_zscore()
print(f'Z-Score: {z_score}')
