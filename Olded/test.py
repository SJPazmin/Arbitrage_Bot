import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from mt5_data import get_data
import MetaTrader5 as mt5
from logger import log
from func_cointegration import *


def calculate_zscore(spread):
    """
    Calculates the Z-score of a given spread series.

    Args:
        spread (pd.Series): The input spread series.

    Returns:
        pd.Series: The Z-score of the input spread series.
    """
    log('Calculating Z-score...')
    zscore = (spread - spread.mean()) / spread.std()
    log('Z-score calculated successfully.')
    return zscore


def main():
    log('Starting pair trading analysis...')

    # Define the symbols to download
    symbols = ['EURUSD', 'GBPUSD']

    # Define the timeframe to download
    timeframe = 5

    # Define the data candles to download
    candles = 7200

    # Download the data
    log('Downloading data...')
    df = get_data(symbols, timeframe, candles)
    log('Data downloaded successfully.')

    data_window = 1440

    results = []

    for i in range(data_window, len(df)):

        # Start when we have enough data
        if i < data_window:
            continue

        data = df.iloc[i-data_window:i]

        spread = calculate_spread(data[symbols[0]], data[symbols[1]])
        hedge_ratio = data[symbols[0]].iloc[-1] / data[symbols[1]].iloc[-1]
        zscore = calculate_zscore(spread)
        stationary = is_stationary(spread)
        halflife = calculate_half_life(spread)

        results.append({
            'Datetime': df.index[i],
            'Spread': spread[-1],
            'Hedge Ratio': hedge_ratio,
            'Z-Score': zscore[-1],
            'Stationary': stationary,
            'Halflife': halflife,
            'Symbol_X': data[symbols[0]][-1],
            'Symbol_Y': data[symbols[1]][-1]
        })

    results_df = pd.DataFrame(results)
    results_df.set_index('Datetime', inplace=True)
    results_df.to_csv('results.csv')

    # Plotting
    fig = make_subplots(rows=5, cols=1)

    # Plot Half-Life
    fig.add_trace(
        go.Scatter(x=results_df.index,
                   y=results_df['Halflife'], name='Half-Life'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=results_df.index,
                   y=results_df['Z-Score'], name='Z-Score'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=results_df.index,
                   y=results_df['Symbol_X'], name=symbols[0]),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(x=results_df.index,
                   y=results_df['Symbol_Y'], name=symbols[1]),
        row=4, col=1
    )

    fig.add_trace(
        go.Scatter(x=results_df.index,
                   y=results_df['Hedge Ratio'], name='Hedge Ratio'),
        row=5, col=1
    )

    fig.update_layout(title_text="Pair Trading Analysis")
    fig.write_html("pair_trading_analysis.html")

    log('Pair trading analysis completed successfully.')


if __name__ == "__main__":
    main()
