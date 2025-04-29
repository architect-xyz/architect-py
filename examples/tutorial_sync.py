import pprint
import time
from decimal import Decimal

from architect_py.graphql_client.enums import OrderStatus
from architect_py.scalars import OrderDir
from architect_py.utils.nearest_tick import TickRoundMethod

from .common import confirm, connect_client, print_book, print_open_orders

c = connect_client()

venue = "CME"

# find ES markets
symbols = c.search_symbols(execution_venue=venue, search_string="ES")
print("\nFound markets:")

for s in symbols:
    print(f"  • {s}")

symbol = symbols[0]

# Lookup information about a single market
print(f"\nDetails for {symbols[0]}:")
product_info = c.get_product_info(symbol)
assert product_info is not None
pprint.pp(product_info)

# Get market snapshot for a single market
# Market snapshots tell you the current best bid, best ask,
# and other ticker info for the given symbol.
# this function is an alias for get_l1_book_snapshot
print(f"\nMarket snapshot for {product_info.symbol}:")
market_snapshot = c.get_market_snapshot(symbol=symbol, venue=venue)

pprint.pp(market_snapshot)

# Get L2 snapshot for a single market
print(f"\nL2 snapshot for {product_info.symbol}:")
start = time.perf_counter()
book = c.get_l2_book_snapshot(symbol=symbol, venue=venue)
elapsed = time.perf_counter() - start
print(f"Got book snapshot in {elapsed:.4f} seconds\n")
print_book(book)

# Get your accounts
print("\nYour accounts:")
accounts = c.list_accounts()
for account in accounts:
    print(f"  • {account.account.name}")

# Check your open orders
print("\nCurrent open orders:")
orders = c.get_open_orders()
print_open_orders(orders)

# Place a limit order 20% below the best bid
best_bid = market_snapshot.bid_price
assert best_bid is not None
limit_price = best_bid * Decimal(0.8)
quantity = Decimal(1)
account = accounts[0]
order = None

if confirm(
    f"Place a limit order to BUY 1 {symbol} LIMIT {limit_price} on account {account.account.name}?"
):
    order = c.send_limit_order(
        symbol=symbol,
        execution_venue=venue,
        odir=OrderDir.BUY,
        quantity=quantity,
        limit_price=limit_price,
        account=account.account.name,
        price_round_method=TickRoundMethod.ROUND,
    )
assert order is not None
print(f"\nOrder placed with ID: {order.id}")

# Poll order status until rejected or fully executed
while order.status is OrderStatus.OPEN:
    time.sleep(1)
    print(f"...order state: {order.status}")
    order = c.get_order(order.id)
    assert order is not None

# Print final order state
if order.status is OrderStatus.REJECTED:
    print(f"Order was rejected: {order.reject_reason}")
elif order.status is OrderStatus.CANCELED:
    print("Order was canceled")
elif order.status is OrderStatus.OUT:
    print(f"Order was filled for qty: {order.filled_quantity}")
    print(f"Average execution price: {order.average_fill_price}")
