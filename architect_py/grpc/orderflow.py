import asyncio
import contextlib
from typing import TYPE_CHECKING, Any, AsyncGenerator, AsyncIterator, Optional, Union

import grpc.aio

from architect_py.grpc.models.Orderflow.Orderflow import *
from architect_py.grpc.models.Orderflow.OrderflowRequest import *

if TYPE_CHECKING:
    from architect_py.async_client import AsyncClient

_CLOSE_SENTINEL: Any = object()  # internal close marker


class OrderflowChannel:
    """
    Web-socket–like helper around Architect’s bidirectional Orderflow gRPC stream.

    Must call OrderflowManager.start() to open the stream.

    Example usage 1:
        om = client.orderflow(queue_size=2048)   # instantiate
        await om.start()                         # open stream

        await om.place_order(args)
        update = await om.receive()  # receive a single orderflow update
        # to receive continuously, either but in a loop or see example usage 2.
        print("first update:", update)

        await om.close()                         # graceful shutdown, not required

    Example usage 2:
        async with await client.orderflow() as om:  # om.start() happens automatically
            async for update in om:  # this will run until the stream is closed
                print("order update:", update)

    For more advanced usage, see the funding_rate_mean_reversion_algo.py example.
    """

    def __init__(self, client: "AsyncClient", *, max_queue_size: int = 1024) -> None:
        self._client = client
        self._send_q: asyncio.Queue[Union[OrderflowRequest, Any]] = asyncio.Queue(
            maxsize=max_queue_size
        )
        self._receive_q: asyncio.Queue[Orderflow] = asyncio.Queue()
        self._stream_task: Optional[asyncio.Task[None]] = None
        self._grpc_call: Optional[
            grpc.aio.StreamStreamCall[OrderflowRequest, Orderflow]
        ] = None
        self._closed = asyncio.Event()

    async def start(self) -> None:
        """ """
        if self._stream_task is None:
            self._stream_task = asyncio.create_task(
                self._stream_loop(), name="orderflow-stream"
            )

    async def send(self, req: OrderflowRequest) -> None:
        """
        Note that some of the OrderflowRequest types are tagged versions of the classes that exist elsewhere.
        Only use the TAGGED versions, as the untagged versions will not work with the stream.
        """
        await self._send_q.put(req)

    async def receive(self) -> Orderflow:
        """Await the next Orderflow update from the server."""
        return await self._receive_q.get()

    async def close(self) -> None:
        if self._stream_task is None:
            return
        await self._send_q.put(_CLOSE_SENTINEL)

        if self._grpc_call is not None:
            self._grpc_call.cancel()

        self._stream_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._stream_task
        self._stream_task = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __aiter__(self) -> AsyncGenerator[Orderflow, None]:
        return self._iter_updates()

    async def _iter_updates(self) -> AsyncGenerator[Orderflow, None]:
        while not self._closed.is_set():
            try:
                yield await self.receive()
            except asyncio.CancelledError:
                break

    async def _request_iter(self) -> AsyncIterator[OrderflowRequest]:
        while True:
            item = await self._send_q.get()
            if item is _CLOSE_SENTINEL:
                break
            yield item

    async def _stream_loop(self) -> None:
        try:
            async for update in self._grpc_orderflow_stream(self._request_iter()):
                await self._receive_q.put(update)
        finally:
            self._closed.set()

    async def _grpc_orderflow_stream(
        self, request_iterator: AsyncIterator[OrderflowRequest]
    ) -> AsyncGenerator[Orderflow, None]:
        """Low-level wrapper around Architect’s gRPC bidirectional stream."""
        grpc_client = await self._client._core()
        decoder = grpc_client.get_decoder(OrderflowRequestUnannotatedResponseType)

        stub: grpc.aio.StreamStreamMultiCallable = grpc_client.channel.stream_stream(
            OrderflowRequest_route,
            request_serializer=grpc_client.encoder().encode,
            response_deserializer=decoder.decode,
        )

        self._grpc_call = stub(
            request_iterator,
            metadata=(("authorization", f"Bearer {grpc_client.jwt}"),),
        )

        async for update in self._grpc_call:
            yield update
