from asyncio.log import logger
from typing import (
    Any,
    AsyncIterator,
    Optional,
    ParamSpec,
    Protocol,
    Type,
    TypeVar,
    cast,
)
from collections.abc import Callable
from datetime import datetime, timedelta
from urllib.parse import urlparse

import msgspec

import dns.asyncresolver
import dns.resolver
from dns.rdtypes.IN.SRV import SRV

import grpc

import bisect
from decimal import Decimal

from architect_py.graphql_client.client import GraphQLClient


from architect_py.grpc_client.Marketdata.L1BookSnapshot import L1BookSnapshot
from architect_py.grpc_client.Marketdata.L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_client.Marketdata.L2BookSnapshotRequest import (
    L2BookSnapshotRequest,
)
from architect_py.grpc_client.Marketdata.L2BookUpdate import (
    L2BookUpdate,
)
from architect_py.grpc_client.Marketdata.SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from architect_py.grpc_client.Marketdata.SubscribeL2BookUpdatesRequest import (
    SubscribeL2BookUpdatesRequest,
)
from architect_py.grpc_client.definitions import L2BookDiff
from architect_py.scalars import TradableProduct
from architect_py.utils.grpc_root_certificates import grpc_root_certificates


"""
TODO:
- confirm get_historical_candles works and fix if it doesn't work

add information and standardization to the rust enums

- loosen the Order types via pre-processing
    - generally any flattened type with oneOf should be loosened and be put in the definitions file
    - add a __post_init__ to confirm the type is correct

remove duplication of:
    CancelAllOrdersRequest


for decode, don't create your own decoder
use the union types and tag values

The decoder should be reused
but it needs to be instantiated per response type
"""


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, TradableProduct):
        return str(obj)


encoder = msgspec.json.Encoder(enc_hook=enc_hook)
TRes = TypeVar("TRes", covariant=True)
P = ParamSpec("P")


class RequestType(Protocol[P, TRes]):
    @staticmethod
    def get_response_type() -> Type[TRes]: ...

    @staticmethod
    def get_route() -> str: ...

    @staticmethod
    def get_unary_type() -> Any: ...

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...


class GRPCClient:
    jwt: str
    jwt_expiration: datetime

    graphql_client: GraphQLClient
    l1_books: dict[TradableProduct, L1BookSnapshot]
    l2_books: dict[TradableProduct, L2BookSnapshot]
    channel: grpc.aio.Channel

    def __init__(
        self,
        graphql_client: GraphQLClient,
        endpoint: str = "cme.marketdata.architect.co",
    ):
        """
        Please ensure to call the initialize method before using the gRPC client.

        grpc_client = GRPCClient(graphql_client, endpoint)
        await grpc_client.initialize()


        Brave users may create their own requests using the RequestUnary and RequestStream classes
        with the subscribe and request methods.
        The types are correct so if a typechecker such as PyLance is throwing errors,
        it's likely a bug in user code.

        async for snap in self.subscribe(
            RequestType.get_request_helper(), # add args/kwargs here
        ):

        snap = await self.request(
            RequestType.get_request_helper(), # add args/kwargs here
        )
        """
        self.graphql_client = graphql_client

        self.jwt_expiration = datetime(1995, 11, 10)

        self.l1_books: dict[TradableProduct, L1BookSnapshot] = {}
        self.l2_books: dict[TradableProduct, L2BookSnapshot] = {}
        self.endpoint = endpoint

    async def initialize(self) -> Optional[str]:
        """
        Initialize the gRPC channel with the given endpoint.
        Must call this method before using the gRPC client.
        """
        # "binance-futures-usd-m.marketdata.architect.co",
        # "bybit.marketdata.architect.co",
        # "binance.marketdata.architect.co",
        # "cme.marketdata.architect.co",
        self.channel = await self.get_grpc_channel(self.endpoint)

    async def change_channel(self, endpoint: str) -> None:
        self.channel = await self.get_grpc_channel(endpoint)

    async def get_grpc_channel(
        self,
        endpoint: str,
    ) -> grpc.aio.Channel:
        if "://" not in endpoint:
            endpoint = f"http://{endpoint}"
        url = urlparse(endpoint)
        if url.hostname is None:
            raise Exception(f"Invalid endpoint: {endpoint}")

        is_https = url.scheme == "https"
        srv_records: dns.resolver.Answer = await dns.asyncresolver.resolve(
            url.hostname, "SRV"
        )
        if len(srv_records) == 0:
            raise Exception(f"No SRV records found for {url.hostname}")

        record = cast(SRV, srv_records[0])

        connect_str = f"{record.target}:{record.port}"
        if is_https:
            credentials = grpc.ssl_channel_credentials(
                root_certificates=grpc_root_certificates
            )
            options = (("grpc.ssl_target_name_override", "service.architect.xyz"),)
            return grpc.aio.secure_channel(connect_str, credentials, options=options)
        else:
            return grpc.aio.insecure_channel(connect_str)

    async def refresh_grpc_credentials(self, force: bool = False) -> str:
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force is True, refresh the JWT unconditionally.
        """
        if force or datetime.now() > self.jwt_expiration - timedelta(minutes=1):
            try:
                self.jwt = (await self.graphql_client.create_jwt()).create_jwt
                self.jwt_expiration = datetime.now() + timedelta(hours=23)
            except Exception as e:
                logger.error("Failed to refresh gRPC credentials: %s", e)
        return self.jwt

    async def request_l2_book_snapshot(
        self, venue: Optional[str], symbol: str
    ) -> L2BookSnapshot:
        return await self.request(L2BookSnapshotRequest, venue=venue, symbol=symbol)

    def initialize_l1_books(
        self, symbols: list[TradableProduct]
    ) -> list[L1BookSnapshot]:
        if symbols is not None:
            if len(self.l1_books) + len(symbols) > 100:
                raise ValueError(
                    "Not suggestible to watch more than 100 L1 symbols at once, as it may cause performance issues."
                )
            symbols = [symbol for symbol in symbols if symbol not in self.l1_books]

            for symbol in symbols:
                self.l1_books[symbol] = L1BookSnapshot(symbol, 0, 0)
        else:
            raise ValueError("symbols must be a list of TradableProduct")
            # could technically be None, but we don't want to allow that
            # as users should be explicit about what they want to watch

        return [self.l1_books[symbol] for symbol in symbols]

    async def watch_l1_books(self, symbols: list[TradableProduct]) -> None:
        symbols_cast = cast(list[str], symbols)
        async for snap in self.subscribe(
            SubscribeL1BookSnapshotsRequest, symbols=symbols_cast
        ):
            book = self.l1_books[cast(TradableProduct, snap.symbol)]
            update_struct(book, snap)

    def initialize_l2_book(
        self, symbol: TradableProduct, venue: Optional[str]
    ) -> L2BookSnapshot:
        if symbol not in self.l2_books:
            if len(self.l2_books) > 20:
                raise ValueError(
                    "Not suggestible to watch more than 20 L2 symbols at once, as it may cause performance issues."
                )
            self.l2_books[symbol] = L2BookSnapshot([], [], 0, 0, 0, 0)
        return self.l2_books[symbol]

    async def subscribe_l1_books_stream(
        self, symbols: list[str]
    ) -> AsyncIterator[L1BookSnapshot]:
        return self.subscribe(
            SubscribeL1BookSnapshotsRequest,
            symbols=symbols,
        )

    async def subscribe_l2_books_stream(
        self, symbol: TradableProduct, venue: Optional[str]
    ) -> AsyncIterator[L2BookUpdate]:
        decode_function: Callable[[bytes], L2BookUpdate] = (
            lambda buf: msgspec.json.decode(
                buf, type=SubscribeL2BookUpdatesRequest.get_response_type()
            )
        )
        stub = self.channel.unary_stream(
            SubscribeL2BookUpdatesRequest.get_route(),
            request_serializer=encoder.encode,
            response_deserializer=decode_function,
        )
        req = SubscribeL2BookUpdatesRequest(symbol=symbol, venue=venue)
        jwt = await self.refresh_grpc_credentials()
        call = stub(req, metadata=(("authorization", f"Bearer {jwt}"),))
        async for update in call:
            yield update

    async def watch_l2_book(
        self, symbol: TradableProduct, venue: Optional[str]
    ) -> None:
        async for up in self.subscribe_l2_books_stream(symbol, venue):
            if isinstance(up, L2BookDiff):  # elif up.t = "d":  # diff
                if symbol not in self.l2_books:
                    raise ValueError(
                        f"received update before snapshot for L2 book {symbol}"
                    )
                book = self.l2_books[symbol]
                if (
                    up.sequence_id != book.sequence_id
                    or up.sequence_number != book.sequence_number + 1
                ):
                    raise ValueError(
                        f"received update out of order for L2 book {symbol}"
                    )
                L2_update_from_diff(book, up)
            elif isinstance(up, L2BookSnapshot):  # if up.t = "s":
                book = self.l2_books[symbol]
                update_struct(book, up)

    async def subscribe(
        self,
        request_type: Type[RequestType[P, TRes]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> AsyncIterator[TRes]:
        decode_function: Callable[[bytes], TRes] = lambda buf: msgspec.json.decode(
            buf, type=request_type.get_response_type()
        )
        stub = self.channel.unary_stream(
            request_type.get_route(),
            request_serializer=encoder.encode,
            response_deserializer=decode_function,
        )
        req = request_type(*args, **kwargs)
        jwt = await self.refresh_grpc_credentials()
        call = stub(req, metadata=(("authorization", f"Bearer {jwt}"),))
        async for update in call:
            yield update

    async def request(
        self,
        request_type: Type[RequestType[P, TRes]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> TRes:
        decode_function: Callable[[bytes], TRes] = lambda buf: msgspec.json.decode(
            buf, type=request_type.get_response_type()
        )
        stub = self.channel.unary_unary(
            request_type.get_route(),
            request_serializer=encoder.encode,
            response_deserializer=decode_function,
        )
        req = request_type(*args, **kwargs)
        jwt = await self.refresh_grpc_credentials()
        return await stub(req, metadata=(("authorization", f"Bearer {jwt}"),))


def update_order_list(
    order_list: list[list[Decimal]],
    price: Decimal,
    size: Decimal,
    ascending: bool,
) -> None:
    """
    Updates a sorted order list (either ascending for asks or descending for bids)
    using binary search to insert, update, or remove the given price level.
    """
    if ascending:
        idx = bisect.bisect_left(order_list, [price, Decimal(0)])
    else:
        lo, hi = 0, len(order_list)
        while lo < hi:
            mid = (lo + hi) // 2
            if order_list[mid][0] > price:
                lo = mid + 1
            else:
                hi = mid
        idx = lo

    if idx < len(order_list) and order_list[idx][0] == price:
        if size.is_zero():
            order_list.pop(idx)
        else:
            # Update the size.
            order_list[idx][1] = size
    else:
        if not size.is_zero():
            order_list.insert(idx, [price, size])


def L2_update_from_diff(book: L2BookSnapshot, diff: L2BookDiff) -> None:
    """
    we use binary search because the L2 does not have many levels
    and is simpler to maintain in the context of the codegen
    """

    book.timestamp = diff.timestamp
    book.timestamp_ns = diff.timestamp_ns
    book.sequence_id = diff.sequence_id
    book.sequence_number = diff.sequence_number

    for price, size in diff.bids:
        update_order_list(book.bids, price, size, ascending=False)

    for price, size in diff.asks:
        update_order_list(book.asks, price, size, ascending=True)


def update_struct(A: msgspec.Struct, B: msgspec.Struct) -> None:
    for field in B.__struct_fields__:
        setattr(A, field, getattr(B, field))
