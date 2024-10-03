import os
import json
import logging
from statistical_functions import ForexStats
from mt5_data import get_data
from constants import WINDOW_LENGTH
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Initialize logger
logger = logging.getLogger(__name__)

# Define output subfolder
output_folder = 'output_folder'
os.makedirs(output_folder, exist_ok=True)

# Load the pair list from the json file
with open('pairs_corr.json', 'r') as file:
    pairs = json.load(file)

# Iterate over all pairs
for pair in pairs:
    logger.info(f'Processing pair: {pair}')

    # Get the data for the current pair
    data = get_data(pair, 5, 28800 + WINDOW_LENGTH, 'close', 'dataframe')

    # Perform the analysis for every window of close prices
    results_list = []
    for i in range(WINDOW_LENGTH, len(data)):
        # Get the close prices for the current window
        window_data = data.iloc[i-WINDOW_LENGTH:i]

        # Convert the close prices to numpy arrays
        arr1 = np.array(window_data.iloc[:, 0])
        arr2 = np.array(window_data.iloc[:, 1])

        # Initialize the ForexStats class with the data
        forex_stats = ForexStats(arr1, arr2)

        # Calculate the spread and z-score
        spread = forex_stats.calculate_spread()
        z_score = forex_stats.calculate_zscore()
        z_score_rolling = forex_stats.calculate_zscore_rolling()

        # Calculate the other statistical values and append all to the results DataFrame
        results_list.append([
            window_data.index[-1],
            arr1[-1],
            arr2[-1],
            forex_stats.calculate_correlation(),
            forex_stats.check_cointegration(),
            spread[-1],
            z_score[-1],
            z_score_rolling[-1],
            forex_stats.calculate_half_life(),
            forex_stats.calculate_hedge_ratio()
        ])

    # Convert results to DataFrame
    results = pd.DataFrame(results_list, columns=[
        'Date', f'{pair[0]} Close', f'{pair[1]} Close', 'Correlation', 'Is Cointegrated',
        'Spread', 'Z-Score', 'Z-Score Rolling', 'Half-Life', 'Hedge Ratio']).set_index('Date')

    # Save the current results to a CSV file
    results.to_csv(os.path.join(
        output_folder, f'{pair[0]}_{pair[1]}_backtest_results.csv'))
    logger.info(f'Saved results to {output_folder}/{pair[0]}_{pair[1]}_backtest_results.csv')

    # Create subplot layout
    fig = make_subplots(
        rows=9,
        cols=1,
        shared_xaxes=True,
        subplot_titles=(f'{pair[0]} Close', f'{pair[1]} Close', 'Correlation',
                        'Is Cointegrated', 'Spread', 'Z-Score', 'Z-Score Rolling',
                        'Half-Life', 'Hedge Ratio'),
        vertical_spacing=0.05)

    # Add traces
    for i, column in enumerate(results.columns):
        fig.add_trace(go.Scatter(x=results.index,
                      y=results[column], name=column), row=i+1, col=1)

    # Add horizontal lines at z-score levels -2, 0, +2
    fig.add_shape(
        type="line", line=dict(dash='dash'),
        xref="paper", yref="y6",
        x0=0, y0=-2, x1=1, y1=-2,
    )
    fig.add_shape(
        type="line", line=dict(dash='dash'),
        xref="paper", yref="y6",
        x0=0, y0=0, x1=1, y1=0,
    )
    fig.add_shape(
        type="line", line=dict(dash='dash'),
        xref="paper", yref="y6",
        x0=0, y0=2, x1=1, y1=2,
    )

    # Update layout
    fig.update_layout(
        height=2500, title_text=f"{pair[0]} and {pair[1]} Backtest Results", showlegend=False)

    # Save to HTML
    fig.write_html(os.path.join(
        output_folder, f'{pair[0]}_{pair[1]}_backtest_results.html'))
    logger.info(f'Saved HTML to {output_folder}/{pair[0]}_{pair[1]}_backtest_results.html')
