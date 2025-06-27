"""
Do *NOT* run this script in production. This script is for educational purposes only.
"""

import asyncio
from decimal import Decimal
from typing import Optional

from architect_py import (
    AsyncClient,
    OrderDir,
    OrderType,
    TimeInForce,
    TradableProduct,
)
from architect_py.grpc.models.Orderflow.Orderflow import (
    TaggedOrderAck,
    TaggedOrderOut,
    TaggedOrderReject,
)
from architect_py.grpc.models.Orderflow.OrderflowRequest import (
    PlaceOrder,
)
from architect_py.grpc.orderflow import OrderflowChannel

from .config import connect_async_client

venue = "BINANCE"
product = "BTC-USDT Perpetual"
tradable_product = TradableProduct(product, "USDT Crypto")
best_bid_price: Optional[Decimal] = None
best_ask_price: Optional[Decimal] = None
current_funding_rate: Optional[Decimal] = None  # as fraction, e.g. 0.0001 = 1 bp
target_position = 0
current_position = 0


async def update_marketdata(c: AsyncClient):
    while True:
        ticker = await c.get_ticker(tradable_product, venue)
        if ticker.funding_rate:
            global current_funding_rate
            global target_position
            current_funding_rate = ticker.funding_rate
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
        if ticker.bid_price:
            global best_bid_price
            best_bid_price = ticker.bid_price
        if ticker.ask_price:
            global best_ask_price
            best_ask_price = ticker.ask_price
        await asyncio.sleep(1)


async def subscribe_and_print_orderflow(
    c: AsyncClient, orderflow_manager: OrderflowChannel
):
    """
    subscribe_orderflow_stream is a duplex_stream meaning that it is a stream that can be read from and written to.
    This is a stream that will be used to send orders to the Architect and receive order updates from the Architect.
    """
    async for orderflow in orderflow_manager:
        if isinstance(orderflow, TaggedOrderAck):
            print(f"<!> ACK {orderflow.order_id}")
        if isinstance(orderflow, TaggedOrderReject):
            print(f"<!> REJECT {orderflow.id} {orderflow.r}: {orderflow.rm}")
            # reject reason, reject message
        elif isinstance(orderflow, TaggedOrderOut):
            print(f"<!> OUT {orderflow.id}")


async def step_to_target_position(c: AsyncClient, orderflow_manager: OrderflowChannel):
    while True:
        await asyncio.sleep(10)
        # check open orders
        open_orders = await c.get_open_orders()
        n = len(open_orders)
        if n > 0:
            print("there are {n} open orders, skipping step")
            continue

        order = None
        # send orders to step to target position
        if current_position < target_position:
            if best_ask_price is not None:
                # buy 1 contract

                # make sure to import the correct PlaceOrder from architect_py.grpc_client.Orderflow.OrderflowRequest
                order = PlaceOrder.new(
                    symbol=tradable_product,
                    dir=OrderDir.BUY,
                    quantity=Decimal(1),
                    execution_venue=None,
                    limit_price=best_ask_price,
                    time_in_force=TimeInForce.DAY,
                    order_type=OrderType.LIMIT,
                )

        elif current_position > target_position:
            if best_bid_price is not None:
                # sell 1 contract

                # make sure to import the correct PlaceOrder from architect_py.grpc_client.Orderflow.OrderflowRequest
                order = PlaceOrder.new(
                    symbol=tradable_product,
                    dir=OrderDir.SELL,
                    quantity=Decimal(1),
                    execution_venue=None,
                    limit_price=best_bid_price,
                    time_in_force=TimeInForce.DAY,
                    order_type=OrderType.LIMIT,
                )

        if order is not None:
            await orderflow_manager.send(
                order
            )  # this will add the order to the queue to send over


async def print_info(c: AsyncClient):
    accounts = await c.list_accounts()
    while True:
        await asyncio.sleep(3)
        account_summaries = await c.get_account_summaries(
            accounts=[account.account.name for account in accounts]
        )
        pos = Decimal(0)
        for account in account_summaries:
            for name, balance in account.balances.items():
                print(f"balance for {name}: {balance}")
                pos += balance
        global current_position
        current_position = pos
        print("---")
        print(f"info : funding_rate: {current_funding_rate}")
        print(f"info : bbo: {best_bid_price} {best_ask_price}")
        print(f"info : current_position: {current_position}")
        print(f"info : target_position: {target_position}")


async def main():
    c = await connect_async_client()

    orderflow_channel = await c.orderflow()
    await orderflow_channel.start()

    await asyncio.gather(
        update_marketdata(c),
        step_to_target_position(c, orderflow_channel),
        print_info(c),
        subscribe_and_print_orderflow(c, orderflow_channel),
    )
    await c.close()


asyncio.run(main())
