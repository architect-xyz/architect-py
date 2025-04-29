import asyncio
from decimal import Decimal

from architect_py.async_client import OrderDir
from architect_py.graphql_client.enums import OrderStatus
from architect_py.scalars import TradableProduct
from examples.common import connect_async_client


async def main():
    c = await connect_async_client()

    market = TradableProduct("ES 20281215 CME Future/US")
    execution_venue = "CME"

    # Get market snapshot for a single market
    # Market snapshots tell you the current best bid, best ask,
    # and other ticker info for the given symbol.
    print()
    print(f"Market snapshot for {market}")
    market_snapshot = await c.get_market_snapshot(symbol=market, venue=execution_venue)
    print(f"Best bid: {market_snapshot.bid_price}")
    print(f"Best ask: {market_snapshot.ask_price}")

    # List your FCM accounts
    print()
    print("Your FCM accounts:")
    accounts = await c.list_accounts()
    for account in accounts:
        print(f"{account.account.name}")

    account_id = accounts[0].account.id

    # Place a limit order $100 below the best bid
    best_bid = market_snapshot.bid_price
    if best_bid is None:
        raise ValueError("No bid price available")
    limit_price = best_bid - Decimal(100)
    quantity = Decimal(1)
    account = accounts[0]
    order = None
    print()
    if (
        input(
            f"Place a limit order to BUY 1 LIMIT {limit_price} on account {account.account.name}? [y/N]"
        )
        == "y"
    ):
        order = await c.send_limit_order(
            symbol=market,
            execution_venue=execution_venue,
            odir=OrderDir.BUY,
            quantity=quantity,
            limit_price=limit_price,
            account=str(account_id),
        )
    else:
        raise ValueError("Order was not placed")
    print(f"Order placed with ID: {order.id}")

    # Poll order status until rejected or fully executed
    # After 5 seconds, cancel the order
    i = 0
    while order.status is OrderStatus.OPEN:
        await asyncio.sleep(1)
        print(f"...order state: {order.status}")
        order = await c.get_order(order.id)
        assert order is not None
        i += 1
        if i == 5:
            print("Canceling order")
            await c.cancel_order(order.id)

    if order.status is OrderStatus.REJECTED:
        print(f"Order was rejected: {order.reject_reason}")
    elif order.status is OrderStatus.CANCELED:
        print("Order was canceled")
    elif order.status is OrderStatus.OUT:
        print(f"Order was filled for qty: {order.filled_quantity}")
        print(f"Average execution price: {order.average_fill_price}")


if __name__ == "__main__":
    asyncio.run(main())
