# PairTrading_Forex

## Overview
This project is a Forex Pair Trading bot that uses statistical methods to identify and trade cointegrated currency pairs. The bot fetches data from MetaTrader 5, performs statistical analysis, and places trades based on the results.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/SJPazmin/Arbitrage_Bot.git
    cd Arbitrage_Bot
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Connect to MetaTrader 5:
    ```python
    from mt5_connector import connect_to_mt5
    connect_to_mt5()
    ```
2. Fetch data for a pair of symbols:
    ```python
    from mt5_data import get_data
    data = get_data(['EURUSD', 'GBPUSD'], 5, 288, 'close', 'dataframe')
    ```
3. Perform statistical analysis:
    ```python
    from statistical_functions import ForexStats
    import numpy as np

    arr1 = np.array(data.iloc[:, 0])
    arr2 = np.array(data.iloc[:, 1])
    forex_stats = ForexStats(arr1, arr2)

    correlation = forex_stats.calculate_correlation()
    is_cointegrated = forex_stats.check_cointegration()
    spread = forex_stats.calculate_spread()
    half_life = forex_stats.calculate_half_life()
    hedge_ratio = forex_stats.calculate_hedge_ratio()
    z_score = forex_stats.calculate_zscore()
    ```
4. Place a market order:
    ```python
    from mt5_positions import place_market_order
    order_ticket = place_market_order("EURUSD", "buy", 0.01)
    ```

## Contributing
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Create a new Pull Request.

## Examples
### Running the scripts
To run the `main.py` script, simply execute:
```bash
python main.py
```

### Interpreting the results
The results of the backtest will be saved in the `output_folder` as CSV and HTML files. The CSV files contain the statistical analysis results for each pair, while the HTML files provide visualizations of the data.

## License
This project is licensed under the MIT License.
