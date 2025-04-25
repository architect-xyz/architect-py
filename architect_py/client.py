import asyncio
import sys
import threading
from asyncio import AbstractEventLoop
from functools import partial
from typing import Any, Awaitable, Callable, Coroutine, Optional, TypeVar

from .async_client import AsyncClient
from .client_interface import ClientProtocol

T = TypeVar("T")


def is_async_function(obj):
    # can be converted to C function for faster performance
    # asyncio.iscoroutinefunction is more comprehensive but almost 3x slower
    return callable(obj) and hasattr(obj, "__code__") and obj.__code__.co_flags & 0x80


class Client(ClientProtocol):
    """
    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    This Client takes control of the event loop, which you can pass in.

    One can find the function definition in the AsyncClient class.

    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.

    Avoid adding functions or other attributes to this class unless you know what you are doing, because
    the __getattribute__ method changes the behavior of the class in a way that is not intuitive.

    Instead, add them to the AsyncClient class.
    """

    __slots__ = ("client", "_event_loop")
    client: AsyncClient
    _event_loop: AbstractEventLoop

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        paper_trading: bool,
        endpoint: str = "https://app.architect.co",
        graphql_port: Optional[int] = None,
        event_loop: Optional[AbstractEventLoop] = None,
        **kwargs,
    ):
        if event_loop is None:
            try:
                event_loop = asyncio.get_running_loop()
            except RuntimeError:
                event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(event_loop)
        super().__setattr__("_event_loop", event_loop)

        async_client = self._event_loop.run_until_complete(
            AsyncClient.connect(
                api_key=api_key,
                api_secret=api_secret,
                paper_trading=paper_trading,
                endpoint=endpoint,
                graphql_port=graphql_port,
                **kwargs,
            )
        )
        super().__setattr__(
            "client",
            async_client,
        )

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
            .__getattribute__("_event_loop")
            .run_until_complete(async_method(*args, **kwargs))
        )


class AsyncExecutor:
    def __init__(self):
        # NB: one consideration is to enforce this class to be a singleton.
        #
        # However, this is not necessary as the class is only used in the
        # Client class when it is used in a jupyter notebook, so its unlikely
        # to be a problem.
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
