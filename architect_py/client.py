import asyncio

import sys
import threading
from asyncio import AbstractEventLoop
from functools import partial
from typing import Any, Awaitable, Callable, Coroutine, Optional, TypeVar

from architect_py.async_client import AsyncClient
from .client_protocol import AsyncClientProtocol


T = TypeVar("T")


def is_async_function(obj):
    # can be converted to C function for faster performance
    # asyncio.iscoroutinefunction is more comprehensive but almost 3x slower
    return callable(obj) and hasattr(obj, "__code__") and obj.__code__.co_flags & 0x80


class Client(AsyncClientProtocol):
    """
    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    One can find the function definition in the AsyncClient class.

    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.

    Avoid adding functions or other attributes to this class unless you know what you are doing, because
    the __getattribute__ method changes the behavior of the class in a way that is not intuitive.

    Instead, add them to the AsyncClient class.
    """

    __slots__ = ("client", "_loop")
    client: AsyncClient
    _loop: AbstractEventLoop

    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        host: str = "app.architect.co",
        paper_trading: bool = True,
        loop: Optional[AbstractEventLoop] = None,
        **kwargs,
    ):
        super().__setattr__(
            "client",
            AsyncClient(
                api_key=api_key,
                api_secret=api_secret,
                host=host,
                paper_trading=paper_trading,
                _i_know_what_i_am_doing=True,
                **kwargs,
            ),
        )

        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        super().__setattr__("_loop", loop)

        if "ipykernel" in sys.modules:
            # for jupyter notebooks
            import atexit

            executor = AsyncExecutor()
            atexit.register(executor.shutdown)

            def _sync_call_create_task(
                async_method: Callable[..., Coroutine[Any, Any, T]],
                *args,
                **kwargs,
            ) -> T:
                """
                Executes the given coroutine synchronously using the executor.
                """
                return executor.submit(async_method(*args, **kwargs))

            super().__setattr__("_sync_call", _sync_call_create_task)

    def __getattribute__(self, name: str):
        """
        You may have been lead here looking for the definition of a method of the Client
        It can be found if you look in the AsyncClient class, which this class is a wrapper for,
        or GraphQLClient, which is a parent class of AsyncClient

        Explanation:
        __getattribute__ is a magic method that is called when searching for any attribute
        In this case, will look through self.client, which is an instance of the Client class

        We do this because we want to be able to call the async methods of the Client in a synchronous way,
        but otherwise pass through the other attributes normally

        It must be getattribute and not getattr because of the AsyncClientProtocol class inheritance
        We gain type hinting but lose the ability to call the methods of the Client class itself
        in a normal way
        """
        attr = getattr(super().__getattribute__("client"), name)
        if is_async_function(attr):
            if "subscribe" in name:
                raise AttributeError(
                    f"Method {name} is an subscription based async method and cannot be called synchronously"
                )
            return partial(super().__getattribute__("_sync_call"), attr)
        else:
            return attr

    def __setattr__(self, name: str, value: Any):
        """primarily to prevent unintended shadowing"""
        client = super().__getattribute__("client")
        setattr(client, name, value)

    def _sync_call(
        self, async_method: Callable[..., Awaitable[T]], *args, **kwargs
    ) -> T:
        return (
            super()
            .__getattribute__("_loop")
            .run_until_complete(async_method(*args, **kwargs))
        )


class AsyncExecutor:
    def __init__(self):
        """
        one consideration is to enforce this class to be a singleton
        however, this is not necessary as the class is only used in the Client class
        when it is used in a jupyter notebook, so unlikely to be a problem
        """

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def submit(self, coro: Coroutine[Any, Any, Any]) -> Any:
        """
        Submit a coroutine to the event loop and wait for its result synchronously.
        """
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    def shutdown(self):
        """
        Shutdown the event loop and background thread gracefully.
        """
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
