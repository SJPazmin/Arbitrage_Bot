from mt5_positions import place_market_order, close_order_by_ticket
from mt5_data import get_data, get_spread, get_time

# Test get_data function
data = get_data(["EURUSD", "GBPUSD"], 5, 10, "close", "dataframe")
# print(data)

# Test get_spread function
spread = get_spread("EURUSD")
print(f"Spread for EURUSD is {spread}")

# Test get_time function
time = get_time("EURUSD")
print(f"Time for EURUSD is {time}")
# Print type of time
print(type(time))

# Test place_market_order function
order_ticket = place_market_order("EURUSD", "buy", 0.01)
if order_ticket != 0:
    print(f"Order placed successfully with ticket {order_ticket}")
else:
    print("Order placement failed")

# Test close_order_by_ticket function
if close_order_by_ticket(order_ticket):
    print(f"Order {order_ticket} closed successfully")
else:
    print(f"Failed to close order {order_ticket}")
