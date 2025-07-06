import asyncio
import logging
import random
import string

from architect_py import (
    Cancel,
    CptyLoginRequest,
    CptyLogoutRequest,
    Order,
)
from architect_py.async_cpty import *


class ExampleCpty(AsyncCpty):
    def __init__(self):
        super().__init__("EXAMPLE")
        # start a mock marketdata task
        asyncio.create_task(mock_marketdata(self))

    async def on_login(self, request: CptyLoginRequest):
        print(
            f"👋 got login request from trader={request.trader} and account={request.account}"
        )

    async def on_logout(self, request: CptyLogoutRequest):
        print("👋 got logout request")

    async def on_place_order(self, order: Order):
        # pretend we're connected to something, ack the order within 1s,
        # then randomly out or fill the order after 3s
        print(f"🎟️ place order: {order}")
        asyncio.create_task(mock_order_lifecycle(self, order))

    async def on_cancel_order(
        self, cancel: Cancel, _original_order: Optional[Order] = None
    ):
        self.reject_cancel(
            cancel.cancel_id,
            reject_reason="cancels always get rejected in this example",
        )

    async def get_open_orders(self) -> Sequence[Order]:
        return []


def random_id(length=10):
    CHARS = string.ascii_uppercase + string.digits
    return "".join(random.choice(CHARS) for _ in range(length))


async def mock_order_lifecycle(cpty: ExampleCpty, order: Order):
    await asyncio.sleep(1)
    exchange_order_id = random_id()
    print(f"🎟️ ack order: {order.id} with exchange_order_id={exchange_order_id}")
    cpty.ack_order(order.id, exchange_order_id=exchange_order_id)

    await asyncio.sleep(3)
    if random.random() < 0.5:
        now = datetime.now()
        print(f"🎟️ fill order: {order.id}")
        cpty.fill_order(
            order_id=order.id,
            exchange_fill_id=random_id(),
            dir=order.dir,
            price=Decimal(13.37),
            quantity=order.quantity,
            symbol=order.symbol,
            trade_time=now,
            account=order.account,
            is_taker=True,
        )
    else:
        print(f"🎟️ out order: {order.id}")
        cpty.out_order(order.id, canceled=False)


async def mock_marketdata(cpty: ExampleCpty):
    while True:
        await asyncio.sleep(0.5)
        bid_price = Decimal(str(random.uniform(12.0, 13.0)))
        ask_price = bid_price + Decimal(str(random.uniform(0.5, 1.0)))
        bid_size = Decimal(str(random.randint(50, 500)))
        ask_size = Decimal(str(random.randint(50, 500)))

        # Generate 3 more levels each side
        bids = [[bid_price, bid_size]]
        asks = [[ask_price, ask_size]]

        for i in range(3):
            # Each level gets slightly worse price
            next_bid = bid_price - Decimal(str(random.uniform(0.1, 0.3))) * (i + 1)
            next_ask = ask_price + Decimal(str(random.uniform(0.1, 0.3))) * (i + 1)
            next_bid_size = Decimal(str(random.randint(50, 500)))
            next_ask_size = Decimal(str(random.randint(50, 500)))
            bids.append([next_bid, next_bid_size])
            asks.append([next_ask, next_ask_size])

        cpty.on_l2_book_snapshot(
            symbol="TEST/USD", timestamp=datetime.now(), bids=bids, asks=asks
        )


async def serve():
    cpty = ExampleCpty()
    await cpty.serve("[::]:50051")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(serve())
