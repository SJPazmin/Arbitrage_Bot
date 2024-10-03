import MetaTrader5 as mt5
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

VALID_DATA_TYPES = ('close', 'open', 'high', 'low', 'volume')
VALID_OUTPUT_FORMATS = ('dataframe', 'csv', 'json')

COLUMN_MAP = {
    'close': ('open', 'high', 'low', 'tick_volume', 'spread', 'real_volume'),
    'open': ('close', 'high', 'low', 'tick_volume', 'spread', 'real_volume'),
    'high': ('open', 'close', 'low', 'tick_volume', 'spread', 'real_volume'),
    'low': ('open', 'high', 'close', 'tick_volume', 'spread', 'real_volume'),
    'volume': ('open', 'high', 'low', 'close', 'spread')
}


def connect_and_execute(func):
    def wrapper(*args, **kwargs):
        connect_to_mt5()
        return func(*args, **kwargs)
    return wrapper


def check_input_validity(symbols, data_type, output_format):
    if not isinstance(symbols, list):
        logging.error("symbols argument must be a list")
        raise TypeError("symbols argument must be a list")
    if data_type not in VALID_DATA_TYPES:
        logging.error(f"data_type argument must be one of {VALID_DATA_TYPES}")
        raise ValueError(
            f"data_type argument must be one of {VALID_DATA_TYPES}")
    if output_format not in VALID_OUTPUT_FORMATS:
        logging.error(
            f"output_format argument must be one of {VALID_OUTPUT_FORMATS}")
        raise ValueError(
            f"output_format argument must be one of {VALID_OUTPUT_FORMATS}")


def process_data_frame(df, symbol, data_type):
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    columns_to_drop = [
        col for col in COLUMN_MAP[data_type] if col in df.columns]

    df.drop(columns=columns_to_drop, inplace=True)
    df.columns = [symbol]

    return df


def get_data_for_symbol(symbol, timeframe, count, data_type):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

    if rates is None:
        logging.error(f"Failed to get rates for {symbol} {timeframe}")
        return pd.DataFrame()

    return process_data_frame(pd.DataFrame(rates), symbol, data_type)


@connect_and_execute
def get_data(symbols, timeframe, count, data_type='close', output_format='dataframe') -> pd.DataFrame:
    check_input_validity(symbols, data_type, output_format)

    try:
        data = pd.concat(
            [get_data_for_symbol(symbol, timeframe, count, data_type) for symbol in symbols], axis=1)
        data.dropna(inplace=True)
        logging.info(f"Fetched data for symbols: {symbols}")
        return get_output(data, output_format)
    except Exception as e:
        logging.error(f"Error fetching data for symbols {symbols}: {str(e)}")
        return pd.DataFrame()


def get_output(data, output_format):
    if output_format == 'dataframe':
        return data
    elif output_format == 'csv':
        return data.to_csv('Data.csv', index=True, header=True)
    elif output_format == 'json':
        return data.to_json()


@connect_and_execute
def get_spread(symbol: str) -> float:
    try:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is not None:
            logging.info(f"Fetched spread for symbol: {symbol}")
            return symbol_info.spread
        else:
            logging.error(f"Error getting spread of {symbol}, returning 0")
            return 0
    except Exception as e:
        logging.error(f"Error fetching spread for symbol {symbol}: {str(e)}")
        return 0


@connect_and_execute
def get_time(symbol: str, timeframe: int = mt5.TIMEFRAME_M5) -> int:
    try:
        time = pd.DataFrame(mt5.copy_rates_from_pos(
            symbol, timeframe, 0, 1)).loc[:, ['time']]
        time = time['time'].iloc[0]
        logging.info(f"Fetched time for symbol: {symbol}")
        return time
    except Exception as e:
        logging.error(
            f"Failed to get time for {symbol} {timeframe}. Error: {str(e)}")
        return 0
