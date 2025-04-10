import asyncio
import pytest

from architect_py.async_client import AsyncClient
from architect_py.grpc_client.Orderflow.OrderflowRequest import OrderflowRequest


class OrderflowAsyncIterator:
    queue: list[OrderflowRequest]
    condition: asyncio.Condition

    def __init__(self):
        self.queue: list[OrderflowRequest] = []
        self.condition: asyncio.Condition = asyncio.Condition()

    def __aiter__(self):
        return self

    async def __anext__(self) -> OrderflowRequest:
        async with self.condition:
            while not self.queue:
                await self.condition.wait()
            return self.queue.pop(0)

    async def add_to_queue(self, item: OrderflowRequest):
        async with self.condition:
            self.queue.append(item)
            self.condition.notify()


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_subscribe_l1_stream(async_client: AsyncClient):
    oai = OrderflowAsyncIterator()
    async for of in async_client.subscribe_orderflow_duplex(oai):
        assert of is not None
        return
