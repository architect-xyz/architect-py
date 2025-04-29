"""
Do *NOT* run this script in production. This script is for educational purposes only.
"""

import asyncio
from decimal import Decimal
from typing import AsyncIterator, Optional

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from architect_py.grpc_client.definitions import TimeInForceEnum
from architect_py.grpc_client.Marketdata.TickerRequest import TickerRequest
from architect_py.grpc_client.Oms.PlaceOrderRequest import PlaceOrderRequestType
from architect_py.grpc_client.Orderflow.Orderflow import (
    TaggedOrderAck,
    TaggedOrderOut,
    TaggedOrderReject,
)
from architect_py.grpc_client.Orderflow.OrderflowRequest import (
    OrderflowRequest,
    PlaceOrder,
)
from architect_py.scalars import OrderDir, TradableProduct

from .common import connect_async_client

venue = "BINANCE"
product = "BTC-USDT Perpetual"
tradable_product = TradableProduct(product, "USDT Crypto")
best_bid_price: Optional[Decimal] = None
best_ask_price: Optional[Decimal] = None
current_funding_rate: Optional[Decimal] = None  # as fraction, e.g. 0.0001 = 1 bp
target_position = 0
current_position = 0


class OrderflowRequester:
    def __init__(self):
        self.queue: asyncio.Queue[OrderflowRequest] = asyncio.Queue()

    async def __aiter__(self) -> AsyncIterator[OrderflowRequest]:
        while True:
            value = await self.queue.get()  # Wait for a value
            yield value  # Yield it when available

    async def __anext__(self) -> OrderflowRequest:
        return await self.queue.get()

    async def put(self, value: OrderflowRequest) -> None:
        # OrderflowRequest contains: PlaceOrder, CancelOrder, CancelAllOrders
        await self.queue.put(value)  # Put value into the queue


async def update_marketdata(c: AsyncClient):
    ticker_request = TickerRequest(symbol=tradable_product)
    s = c.grpc_client.subscribe(ticker_request)
    async for ticker in s:
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


async def subscribe_and_print_orderflow(
    c: AsyncClient, orderflow_requester: OrderflowRequester
):
    try:
        stream = c.grpc_client.subscribe_orderflow_stream(orderflow_requester)
        """
        subscribe_orderflow_stream is a duplex_stream meaning that it is a stream that can be read from and written to.
        This is a stream that will be used to send orders to the Architect and receive order updates from the Architect.
        """
        async for orderflow in stream:
            if isinstance(orderflow, TaggedOrderAck):
                print(f"<!> ACK {orderflow.order_id}")
            if isinstance(orderflow, TaggedOrderReject):
                print(f"<!> REJECT {orderflow.id} {orderflow.r}: {orderflow.rm}")
                # reject reason, reject message
            elif isinstance(orderflow, TaggedOrderOut):
                print(f"<!> OUT {orderflow.id}")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def step_to_target_position(
    c: AsyncClient, orderflow_requester: OrderflowRequester
):
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
                    time_in_force=TimeInForceEnum.DAY,
                    place_order_request_type=PlaceOrderRequestType.LIMIT,
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
                    time_in_force=TimeInForceEnum.DAY,
                    place_order_request_type=PlaceOrderRequestType.LIMIT,
                )

        if order is not None:
            await orderflow_requester.put(
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
            for balance in account.balances:
                if balance.product is None:
                    name = "UNKNOWN NAME"
                else:
                    name = balance.product
                print(f"balance for {name}: {balance.balance}")
                if name and balance.balance is not None:
                    pos += balance.balance
        global current_position
        current_position = pos
        print("---")
        print(f"info : funding_rate: {current_funding_rate}")
        print(f"info : bbo: {best_bid_price} {best_ask_price}")
        print(f"info : current_position: {current_position}")
        print(f"info : target_position: {target_position}")


async def main():
    c = await connect_async_client()

    orderflow_requester = OrderflowRequester()

    await asyncio.gather(
        update_marketdata(c),
        step_to_target_position(c, orderflow_requester),
        print_info(c),
        subscribe_and_print_orderflow(c, orderflow_requester),
    )


asyncio.run(main())
