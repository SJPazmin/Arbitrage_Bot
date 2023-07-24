import json
import pandas as pd
import numpy as np
from mt5_data import get_data

# Load the pair list from the json file
with open('pairs.json', 'r') as file:
    pairs = json.load(file)

# Define the length of the window for the analysis
window_length = 288

# Initialize a DataFrame to store the results
results_df = pd.DataFrame(
    columns=['Pair', 'Total Windows', 'Highly Correlated Windows'])

# Iterate over all pairs
for pair in pairs:
    print(f'Processing pair: {pair}')

    # Get the data for the current pair
    data = get_data(pair, 5, 34560, 'close', 'dataframe')

    # Initialize counters
    high_correlation_count = 0
    total_windows = 0

    # Perform the analysis for every window of close prices
    for i in range(window_length, len(data)):
        # Get the close prices for the current window
        window_data = data.iloc[i-window_length:i]

        # Convert the close prices to numpy arrays
        arr1 = np.array(window_data.iloc[:, 0])
        arr2 = np.array(window_data.iloc[:, 1])

        # Calculate correlation directly using numpy
        correlation = np.corrcoef(arr1, arr2)[0, 1]

        # Check if correlation is greater than 0.8
        if correlation > 0.8:
            high_correlation_count += 1

        total_windows += 1

    # Record the results
    results_df = pd.concat([results_df, pd.DataFrame({'Pair': [pair], 'Total Windows': [total_windows],
                                                      'Highly Correlated Windows': [high_correlation_count]})], ignore_index=True)

    # Save the results to a csv file
    results_df.to_csv('correlation_results.csv', index=False)

    print(f'Finished processing pair: {pair}')
