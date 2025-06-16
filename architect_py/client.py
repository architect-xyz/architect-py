import asyncio
import sys
import threading
from asyncio import AbstractEventLoop
from collections.abc import Callable
from functools import partial
from typing import (
    Any,
    Concatenate,
    Coroutine,
    Optional,
    ParamSpec,
    Sequence,
    TypeVar,
)

from .async_client import AsyncClient


def is_async_function(obj):
    # can be converted to C function for faster performance
    # asyncio.iscoroutinefunction is more comprehensive but almost 3x slower
    return callable(obj) and hasattr(obj, "__code__") and obj.__code__.co_flags & 0x80


P = ParamSpec("P")
T = TypeVar("T")


class Client:
    """
    One can find the function definition in the AsyncClient class and in the pyi file.

    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    This Client takes control of the event loop, which you can pass in.


    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.
    Avoid adding functions or other attributes to this class unless you know what you are doing.
    """

    __slots__ = (
        "client",
        "_event_loop",
        "_sync_call",
        "__dict__",
    )
    client: AsyncClient
    _event_loop: AbstractEventLoop

    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        paper_trading: bool,
        as_user: Optional[str] = None,
        as_role: Optional[str] = None,
        endpoint: str = "https://app.architect.co",
        graphql_port: Optional[int] = None,
        grpc_options: Sequence[tuple[str, Any]] | None = None,
        event_loop: Optional[AbstractEventLoop] = None,
        **kwargs,
    ):
        """
        Create a new Client instance.

        An `api_key` and `api_secret` can be created at https://app.architect.co/api-keys

        Pass in an `event_loop` if you want to use your own; otherwise, this class
        will use the default asyncio event loop.
        """
        self._sync_call = self._pick_executor()

        if event_loop is None:
            try:
                event_loop = asyncio.get_running_loop()
            except RuntimeError:
                event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(event_loop)
        object.__setattr__(self, "_event_loop", event_loop)

        async_client: AsyncClient = self._sync_call(
            AsyncClient.connect,
            api_key=api_key,
            api_secret=api_secret,
            paper_trading=paper_trading,
            as_user=as_user,
            as_role=as_role,
            endpoint=endpoint,
            graphql_port=graphql_port,
            grpc_options=grpc_options,
            **kwargs,
        )

        object.__setattr__(
            self,
            "client",
            async_client,
        )
        self._promote_async_client_methods()

    def _pick_executor(
        self,
    ) -> Callable[
        Concatenate[Callable[P, Coroutine[Any, Any, T]], P],
        T,
    ]:
        """Return a function that runs a coroutine and blocks."""
        if "ipykernel" in sys.modules:
            executor = AsyncExecutor()
            import atexit

            atexit.register(executor.shutdown)
            return lambda fn, *a, **kw: executor.submit(fn(*a, **kw))

        return lambda fn, *a, **kw: self._event_loop.run_until_complete(fn(*a, **kw))

    def _promote_async_client_methods(self) -> None:
        for name in dir(self.client):
            if name.startswith("_"):
                continue

            if any(x in name for x in ("stream", "subscribe", "connect")):
                continue
            attr = getattr(self.client, name)

            if is_async_function(attr):
                attr = partial(self._sync_call, attr)

            object.__setattr__(self, name, attr)

    def __setattr__(self, name: str, value: Any) -> None:
        # protect wrapper internals
        if name in ("client", "_event_loop", "_sync_call"):
            object.__setattr__(self, name, value)
        else:
            setattr(self.client, name, value)


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
