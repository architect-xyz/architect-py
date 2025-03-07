"""
This example is outdated and will not work with the current version of the library due to
`subscribe_exchange_specific` not existing anymore.

Please contact Architect if you would like this functionality added back.
"""

import asyncio
from decimal import Decimal
from typing import Optional

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from architect_py.scalars import OrderDir, TradableProduct
from architect_py.utils.nearest_tick import TickRoundMethod

from .common import create_async_client


venue = "BINANCE-FUTURES-USD-M"
route = "DIRECT"
product = f"BTC-USDT Perpetual"
tradable_product = TradableProduct(product, "USDT Crypto")
best_bid_price: Optional[Decimal] = None
best_ask_price: Optional[Decimal] = None
current_funding_rate: Optional[Decimal] = None  # as fraction, e.g. 0.0001 = 1 bp
target_position = 0
current_position = 0


# COMING SOON
# async def subscribe_and_print_orderflow(c: AsyncClient):
#     try:
#         stream = c.subscribe_orderflow()
#         async for item in stream:
#             orderflow = getattr(item, "orderflow")
#             if orderflow.typename__ == "Ack":
#                 print(f"<!> ACK {orderflow.order_id}")
#             elif orderflow.typename__ == "Reject":
#                 print(f"<!> REJECT {orderflow.order_id}: {orderflow.reason}")
#             elif orderflow.typename__ == "Out":
#                 print(f"<!> OUT {orderflow.order_id}")
#     except GraphQLClientHttpError as e:
#         print(e.status_code)
#         print(e.response.json())


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
                    order = await c.send_limit_order(
                        symbol=tradable_product,
                        odir=OrderDir.BUY,
                        quantity=Decimal(1),
                        execution_venue=None,
                        limit_price=best_ask_price,
                        price_round_method=TickRoundMethod.ROUND,
                        # account = account
                    )
                    if order is None:
                        raise ValueError("No response")

                    print(f"Order #{order.id}: BUY 1 contract @ {best_ask_price}")
                except GraphQLClientHttpError as e:
                    print(e.response.json())
                    raise e
        elif current_position > target_position:
            if best_bid_price is not None:
                # sell 1 contract
                try:
                    order = await c.send_limit_order(
                        symbol=tradable_product,
                        odir=OrderDir.SELL,
                        quantity=Decimal(1),
                        execution_venue=None,
                        limit_price=best_bid_price,
                        price_round_method=TickRoundMethod.ROUND,
                        # account = account
                    )
                    print(f"Order #{order}: SELL 1 contract @ {best_bid_price}")
                except GraphQLClientHttpError as e:
                    print(e.response.json())
                    raise e


async def print_info(c: AsyncClient):
    accounts = await c.list_accounts()
    while True:
        await asyncio.sleep(3)
        account_summaries = await c.get_account_summaries(
            accounts=[account.account.name for account in accounts]
        )
        pos = 0
        for account in account_summaries:
            for balance in account.balances:
                if balance.product is None:
                    name = "UNKNOWN NAME"
                else:
                    name = balance.product
                print(f"balance for {name}: {balance.balance}")
                if name and balance.balance is not None:
                    pos += float(balance.balance)
        global current_position
        current_position = pos
        print(f"---")
        print(f"info : funding_rate: {current_funding_rate}")
        print(f"info : bbo: {best_bid_price} {best_ask_price}")
        print(f"info : current_position: {current_position}")
        print(f"info : target_position: {target_position}")


async def main():
    c = await create_async_client()
    await asyncio.gather(
        step_to_target_position(c),
        print_info(c),
        # subscribe_and_print_orderflow(c),
    )


asyncio.run(main())
