from decimal import Decimal
import pprint
import time

from architect_py.scalars import OrderDir
from architect_py.utils.nearest_tick import TickRoundMethod

from .common import confirm, create_client, print_book, print_open_orders


c = create_client()

venue = "CME"

# Find all MET markets (Micro ETH) from CME
# markets = c.search_markets(venue="COINBASE", base="BTC Crypto", quote="USD")
symbols = c.search_symbols(venue=venue, underlying="MET CME Index")
print("\nFound markets:\n")
for s in symbols:
    print(f"  • {s}")

# Lookup information about a single market
print(f"\nDetails for {symbols[0]}:")
product_info = c.get_product_info(symbols[0])
assert product_info is not None
pprint.pp(product_info)

# Get market snapshot for a single market
# Market snapshots tell you the current best bid, best ask,
# and other ticker info for the given symbol.
print()
print(f"Market snapshot for {product_info.product_info}:")
print()
market_snapshot = c.market_snapshot(venue, market)

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
best_bid = book.bids[0].price
limit_price = best_bid * Decimal(0.8)
quantity = Decimal(1)
account = accounts[0]
print()
order = None

assert isinstance(market.kind, MarketFieldsKindExchangeMarketKind)

if confirm(
    f"Place a limit order to BUY 1 {market.kind.base.name} LIMIT {limit_price} {market.kind.quote.name} on account {account.name}?"
):
    order = c.send_limit_order(
        market=market.name,
        odir=OrderDir.BUY,
        quantity=quantity,
        limit_price=limit_price,
        account=account.id,
        price_round_method=TickRoundMethod.ROUND,
    )
print()
assert order is not None
print(f"Order placed with ID: {order.order.id}")

# Poll order status until rejected or fully executed
while OrderStateFlags.OPEN in order.order_state:
    time.sleep(1)
    print(f"...order state: {order.order_state}")
    order = c.get_order(order.order.id)
    assert order is not None

# Print final order state
if OrderStateFlags.REJECTED in order.order_state:
    print(f"Order was rejected: {order.reject_reason}")
elif OrderStateFlags.CANCELED in order.order_state:
    print("Order was canceled")
elif OrderStateFlags.FILLED in order.order_state:
    print(f"Order was filled for qty: {order.filled_qty}")
    print(f"Average execution price: {order.avg_fill_price}")
