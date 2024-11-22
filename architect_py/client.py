from asyncio import AbstractEventLoop
import asyncio
from functools import partial
from typing import Awaitable, Callable, Optional, TypeVar

from architect_py.async_client import AsyncClient
from architect_py.protocol.client_protocol import AsyncClientProtocol


T = TypeVar("T")


def is_async_function(obj):
    # can be converted to C function for faster performance
    return callable(obj) and hasattr(obj, "__code__") and obj.__code__.co_flags & 0x80


class Client(AsyncClientProtocol):
    """
    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    One can find the function definition in the AsyncClient class.

    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.
    """

    client: AsyncClient
    loop: AbstractEventLoop

    def __init__(self, loop: Optional[AbstractEventLoop] = None, *args, **kwargs):
        self.client = AsyncClient(*args, **kwargs)

        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        self.loop = loop

    def __getattr__(self, name: str):
        """
        You may have been lead here looking for the definition of a method of the Client
        It can be found if you look in the AsyncClient class, which this class is a wrapper for,
        or GraphQLClient, which is a parent class of AsyncClient

        Explanation:
        __getattr__ is a magic method that is called when an attribute is not found in the class
        In this case, will look through self.client, which is an instance of the Client class

        We do this because we want to be able to call the async methods of the Client in a synchronous way
        """
        attr = getattr(self.client, name)
        if is_async_function(attr):
            if "subscribe" in name:
                raise AttributeError(
                    f"Method {name} is an subscription based async method and cannot be called synchronously"
                )
            return partial(self._sync_call, attr)
        else:
            return attr

    def _sync_call(
        self, async_method: Callable[..., Awaitable[T]], *args, **kwargs
    ) -> T:
        return self.loop.run_until_complete(async_method(*args, **kwargs))


a = Client()

a.find_markets
a.get_l3_book_snapshot
a.subscribe_l1_book_snapshots

a = AsyncClient()

a.find_markets
a.get_l3_book_snapshot
a.subscribe_l1_book_snapshots
