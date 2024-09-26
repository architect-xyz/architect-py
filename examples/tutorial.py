import pprint
import time
from architect_py.client import OrderDirection
from architect_py.graphql_client.enums import OrderStateFlags
from .common import create_client, print_book, print_open_orders, confirm


c = create_client()

# Find all MET markets (Micro ETH) from CME
# markets = c.search_markets(venue="COINBASE", base="BTC Crypto", quote="USD")
markets = c.search_markets(venue="CME", underlying="MET CME Index")
print()
print("Found markets:")
print()
for m in markets:
    print(f"  • {m.name}")

# Lookup information about a single market
print()
print(f"Details for {markets[0].name}:")
print()
market = c.get_market(markets[0].name)
pprint.pp(market)

# Get market snapshot for a single market
# Market snapshots tell you the current best bid, best ask,
# and other ticker info for the given symbol.
print()
print(f"Market snapshot for {market.name}:")
print()
market_snapshot = c.get_market_snapshot(market.name)
pprint.pp(market_snapshot)

# Get book snapshot for a single market
print()
print(f"Book snapshot for {market.name}:")
start = time.perf_counter()
book = c.get_book_snapshot(market.name, num_levels=100)
elapsed = time.perf_counter() - start
print(f"Got book snapshot in {elapsed:.4f} seconds")
print()
print_book(book)

# Get your accounts
print()
print("Your accounts:")
print()
accounts = c.get_accounts()
for account in accounts:
    print(f"  • {account.name}")

# Check your open orders
print()
print("Current open orders:")
print()
orders = c.get_open_orders()
print_open_orders(orders)

# Place a limit order 20% below the best bid
best_bid = float(book.bids[0].price)
limit_price = round(best_bid * 0.8)
quantity = 1.0
account = accounts[0]
print()
order = None
if confirm(
    f"Place a limit order to BUY 1 {market.kind.base.name} LIMIT {limit_price} {market.kind.quote.name} on account {account.name}?"
):
    order = c.send_limit_order(
        market=market.name,
        dir=OrderDirection.BUY,
        quantity=quantity,
        limit_price=limit_price,
        account=account.id,
    )
print()
print(f"Order placed with ID: {order.order.id}")

# Poll order status until rejected or fully executed
while OrderStateFlags.OPEN in order.order_state:
    time.sleep(1)
    print(f"...order state: {order.order_state}")
    order = c.get_order(order.order.id)

# Print final order state
if OrderStateFlags.REJECTED in order.order_state:
    print(f"Order was rejected: {order.reject_reason}")
elif OrderStateFlags.CANCELED in order.order_state:
    print("Order was canceled")
elif OrderStateFlags.FILLED in order.order_state:
    print(f"Order was filled for qty: {order.filled_qty}")
    print(f"Average execution price: {order.avg_fill_price}")
