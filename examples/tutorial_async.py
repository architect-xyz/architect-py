import asyncio
from decimal import Decimal

from architect_py import OrderDir, OrderStatus, OrderType, TradableProduct

from .config import connect_async_client


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
    print(f"Best bid: {market_snapshot.best_bid}")
    print(f"Best ask: {market_snapshot.best_ask}")

    # List your FCM accounts
    print()
    print("Your FCM accounts:")
    accounts = await c.list_accounts()
    for account in accounts:
        print(f"{account.account.name}")

    account_id = accounts[0].account.id

    # Place a limit order $100 below the best bid
    if (best_bid := market_snapshot.best_bid) is not None:
        bid_px = best_bid[0]
    else:
        raise ValueError("No bid price available")

    limit_price = bid_px - Decimal(100)
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
        order = await c.place_order(
            symbol=market,
            execution_venue=execution_venue,
            dir=OrderDir.BUY,
            order_type=OrderType.LIMIT,
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
    while order.status is OrderStatus.Open:
        await asyncio.sleep(1)
        print(f"...order state: {order.status}")
        order = await c.get_order(order.id)
        assert order is not None
        i += 1
        if i == 5:
            print("Canceling order")
            await c.cancel_order(order.id)

    if order.status is OrderStatus.Rejected:
        print(f"Order was rejected: {order.reject_reason}")
    elif order.status is OrderStatus.Canceled:
        print("Order was canceled")
    elif order.status is OrderStatus.Out:
        print(f"Order was filled for qty: {order.filled_quantity}")
        print(f"Average execution price: {order.average_fill_price}")

    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
