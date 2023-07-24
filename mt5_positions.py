import MetaTrader5 as mt5
from mt5_connector import connect_to_mt5

# Define constants for the actions, fillings, and time order settings
ACTION = mt5.TRADE_ACTION_DEAL
FILLING = mt5.ORDER_FILLING_IOC
TIME = mt5.ORDER_TIME_GTC

# This decorator function will ensure that you're connected to MetaTrader 5 before any trading operation


def connect_and_execute(func):
    def wrapper(*args, **kwargs):
        connect_to_mt5()
        return func(*args, **kwargs)
    return wrapper

# This function is used to place a market order


@connect_and_execute
def place_market_order(symbol, type, volume: float, magic_number: int = 0, comment: str = "") -> int:
    # Determine order type based on the input
    order_type = mt5.ORDER_TYPE_BUY if type == "buy" else mt5.ORDER_TYPE_SELL

    # Build the request dict
    request = {
        "action": ACTION,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "magic": magic_number,
        "comment": comment,
        "type_time": TIME,
        "type_filling": FILLING
    }

    # Check if the order request is valid
    check = mt5.order_check(request)
    if check is None or check.retcode != 0:
        print("Order check failed with error code: {}".format(
            check.retcode if check is not None else 'None'))
        return 0

    # Send the order request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order failed with error code: {}".format(result.retcode))
        return 0

    # Return the order number
    return result.order

# This function is used to close an order by its ticket number


@connect_and_execute
def close_order_by_ticket(ticket: int, comment: str = ""):
    # Get the position details
    position_info = mt5.positions_get(ticket=ticket)
    if position_info == ():
        print(f"No positions with ticket {ticket}")
        return False

    # Extract the necessary details from the position
    symbol = position_info[0].symbol
    volume = position_info[0].volume
    order_type = mt5.ORDER_TYPE_BUY if position_info[0].type == 1 else mt5.ORDER_TYPE_SELL
    magic_number = position_info[0].magic

    # Build the request dict
    request = {
        "action": ACTION,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "magic": magic_number,
        "comment": comment,
        "type_time": TIME,
        "type_filling": FILLING
    }

    # Send the close order request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(
            "Position Close failed, retcode={} - {}".format(result.retcode, result.comment))
        return False
    elif result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Position {} Closed on {}, comment = {}".format(
            result.order, request['symbol'], result.comment))
        return True

# This function checks if there are any open orders for the given pair of symbols in the positions dictionary


def check_open_orders(symbol_x, symbol_y, open_positions_dict):
    return any(position["symbol_x"] == symbol_x and position["symbol_y"] == symbol_y for position in open_positions_dict)

# This function checks if a ticket is open or not


@connect_and_execute
def check_open_ticket(ticket: int):
    return mt5.positions_get(ticket=ticket) != ()
