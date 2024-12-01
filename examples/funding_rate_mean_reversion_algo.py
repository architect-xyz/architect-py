import asyncio
from typing import Optional

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError

from .common import create_async_client


venue = "BINANCE-FUTURES-USD-M"
route = "DIRECT"
product = f"BTC-USDT Perpetual"
market = f"{product}/USDT Crypto*{venue}/{route}"
best_bid_price: Optional[float] = None
best_ask_price: Optional[float] = None
current_funding_rate = None  # as fraction, e.g. 0.0001 = 1 bp
target_position = 0
current_position = 0


async def update_marketdata(c: AsyncClient):
    s = c.subscribe_exchange_specific(
        markets=[market],
        fields=["funding_rate", "best_bid_price", "best_ask_price"],
    )
    async for batched in s:
        for update in batched:
            value = None
            if update.value is not None:
                value = float(update.value)
            if update.field == "funding_rate":
                global current_funding_rate
                global target_position
                current_funding_rate = value
                # set target_position based on funding rate
                if current_funding_rate >= 0.1:
                    target_position = -10
                elif current_funding_rate >= 0.05:
                    target_position = -5
                elif current_funding_rate >= 0.0001:
                    target_position = 1
                elif current_funding_rate >= -0.05:
                    target_position = 5
                else:
                    target_position = 10
            elif update.field == "best_bid_price":
                global best_bid_price
                best_bid_price = value
            elif update.field == "best_ask_price":
                global best_ask_price
                best_ask_price = value


async def subscribe_and_print_orderflow(c: AsyncClient):
    try:
        stream = c.subscribe_orderflow()
        async for item in stream:
            if item.orderflow.typename__ == "Ack":
                print(f"<!> ACK {item.orderflow.order_id}")
            elif item.orderflow.typename__ == "Reject":
                print(f"<!> REJECT {item.orderflow.order_id}: {item.orderflow.reason}")
            elif item.orderflow.typename__ == "Out":
                print(f"<!> OUT {item.orderflow.order_id}")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def step_to_target_position(c: AsyncClient):
    while True:
        await asyncio.sleep(10)
        # check open orders
        open_orders = await c.get_open_orders()
        n = len(open_orders)
        if n > 0:
            print("there are {n} open orders, skipping step")
            continue
        # send orders to step to target position
        if current_position < target_position:
            if best_ask_price is not None:
                # buy 1 contract
                try:
                    res = await c.send_limit_order(
                        market=market,
                        side="buy",
                        limit_price=best_ask_price,
                        quantity=1,
                    )
                    order_id = res.create_order
                    print(f"Order #{order_id}: BUY 1 contract @ {best_ask_price}")
                except GraphQLClientHttpError as e:
                    print(e.response.json())
                    raise e
        elif current_position > target_position:
            if best_bid_price is not None:
                # sell 1 contract
                try:
                    res = await c.send_limit_order(
                        market=market,
                        side="sell",
                        limit_price=best_bid_price,
                        quantity=1,
                    )
                    order_id = res.create_order
                    print(f"Order #{order_id}: SELL 1 contract @ {best_bid_price}")
                except GraphQLClientHttpError as e:
                    print(e.response.json())
                    raise e


async def print_info(c: AsyncClient):
    while True:
        await asyncio.sleep(3)
        r = await c.get_balances_for_cpty(venue, route)
        pos = 0
        for balance in r.balances_for_cpty:
            print(f"attn: balance for {balance.product.name}: {balance.amount}")
            if balance.product.name == product:
                pos += float(balance.amount)
        global current_position
        current_position = pos
        print(f"---")
        print(f"info : funding_rate: {current_funding_rate}")
        print(f"info : bbo: {best_bid_price} {best_ask_price}")
        print(f"info : current_position: {current_position}")
        print(f"info : target_position: {target_position}")


async def main():
    c = create_async_client()
    await asyncio.gather(
        update_marketdata(c),
        step_to_target_position(c),
        print_info(c),
        subscribe_and_print_orderflow(c),
    )


asyncio.run(main())
