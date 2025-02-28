from asyncio.log import logger
from typing import Any, AsyncIterator, Optional, cast
from datetime import datetime, timedelta
from urllib.parse import urlparse


import dns.asyncresolver
import dns.resolver
from dns.rdtypes.IN.SRV import SRV

import grpc

import bisect
from decimal import Decimal
from typing import List

from architect_py.graphql_client.client import GraphQLClient


from architect_py.grpc_client.Marketdata.Array_of_L1BookSnapshot import (
    L1BookSnapshot,
)
from architect_py.grpc_client.Marketdata.L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_client.Marketdata.L2BookSnapshotRequest import (
    L2BookSnapshotRequest,
)
from architect_py.grpc_client.Marketdata.L2BookUpdate import (
    Diff,
    L2BookUpdate,
    Snapshot,
)
from architect_py.grpc_client.Marketdata.SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from architect_py.grpc_client.Marketdata.SubscribeL2BookUpdatesRequest import (
    SubscribeL2BookUpdatesRequest,
)
from architect_py.grpc_client.Marketdata.Trade import Trade
from architect_py.protocol.marketdata import JsonMarketdataStub

from architect_py.scalars import TradableProduct
from architect_py.utils.grpc_root_certificates import grpc_root_certificates


"""
TODO:
Custom Code Generation for the gRPC client
    - might fix duplication of types issue
    - might fix the Decimal = str issue
Fix the duplication of types issue in the generated code
"""


class GRPCClient:
    jwt: str
    jwt_expiration: datetime

    graphql_client: GraphQLClient
    l2_books: dict[TradableProduct, Snapshot]
    channel: grpc.aio.Channel

    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client
        self.l2_books: dict[TradableProduct, Snapshot] = {}

    async def initialize(self):
        # "binance-futures-usd-m.marketdata.architect.co",
        # "bybit.marketdata.architect.co",
        # "binance.marketdata.architect.co",
        # "app.architect.co",
        if self.channel is None:
            self.channel = await self.get_grpc_channel("app.architect.co")

        await self.refresh_grpc_credentials()

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

    async def refresh_grpc_credentials(self, force: bool = False) -> Optional[str]:
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force is True, refresh the JWT unconditionally.
        """
        if (
            force
            or self.jwt is None
            or (
                self.jwt_expiration is not None
                and datetime.now() > self.jwt_expiration - timedelta(minutes=1)
            )
        ):
            try:
                self.jwt = (await self.graphql_client.create_jwt()).create_jwt
                self.jwt_expiration = datetime.now() + timedelta(hours=23)
            except Exception as e:
                logger.error("Failed to refresh gRPC credentials: %s", e)

    async def l2_book_snapshot(
        self, venue: Optional[str], symbol: str
    ) -> L2BookSnapshot:
        await self.initialize()

        stub = L2BookSnapshotRequest.create_stub(self.channel)
        req = L2BookSnapshotRequest(venue=venue, symbol=symbol)
        return await stub(req, metadata=(("authorization", f"Bearer {self.jwt}"),))

    async def subscribe_l1_book_snapshots(
        self, symbols: list[str] | None = None
    ) -> AsyncIterator[L1BookSnapshot]:
        stub = SubscribeL1BookSnapshotsRequest.create_stub(self.channel)
        req = SubscribeL1BookSnapshotsRequest(symbols=symbols)
        call = stub(req)
        async for snapshot in call:
            yield snapshot

    async def subscribe_l2_book_updates(
        self,
        symbol: TradableProduct,
        venue: Optional[str],
    ) -> AsyncIterator[L2BookUpdate]:
        stub = SubscribeL2BookUpdatesRequest.create_stub(self.channel)
        req = SubscribeL2BookUpdatesRequest(venue=venue, symbol=symbol)
        jwt = await self.refresh_grpc_credentials()
        call = stub(req, metadata=(("authorization", f"Bearer {jwt}"),))
        async for snapshot in call:
            yield snapshot

    async def watch_l2_book(
        self, symbol: TradableProduct, venue: Optional[str]
    ) -> AsyncIterator[tuple[int, int]]:
        async for up in self.subscribe_l2_book_updates(symbol=symbol, venue=venue):
            if isinstance(up, Snapshot):  # if up.t.value = "s":
                self.l2_books[symbol] = up
            if isinstance(up, Diff):  # elif up.t.value = "d":  # diff
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

            yield (up.sequence_id, up.sequence_number)


def update_order_list(
    order_list: List[List[Decimal]], price: Decimal, size: Decimal, ascending: bool
) -> None:
    """
    Updates a sorted order list (either ascending for asks or descending for bids)
    using binary search to insert, update, or remove the given price level.
    """
    if ascending:
        # For asks: list is sorted in ascending order by price.
        idx = bisect.bisect_left(order_list, [price, Decimal(0)])
    else:
        # For bids: list is sorted in descending order.
        # We perform a custom binary search.
        lo, hi = 0, len(order_list)
        while lo < hi:
            mid = (lo + hi) // 2
            if order_list[mid][0] > price:
                lo = mid + 1
            else:
                hi = mid
        idx = lo

    # Check if the price level exists at the found index.
    if idx < len(order_list) and order_list[idx][0] == price:
        if size.is_zero():
            # Remove the price level.
            order_list.pop(idx)
        else:
            # Update the size.
            order_list[idx][1] = size
    else:
        if not size.is_zero():
            # Insert new price level.
            order_list.insert(idx, [price, size])


def L2_update_from_diff(book: Snapshot, diff: L2BookUpdate) -> None:
    # Update the metadata fields.
    book.timestamp = diff.timestamp
    book.timestamp_ns = diff.timestamp_ns
    book.sequence_id = diff.sequence_id
    book.sequence_number = diff.sequence_number

    # Update bids (assumed sorted descending).
    for price, size in diff.bids:
        update_order_list(book.bids, price, size, ascending=False)

    # Update asks (assumed sorted ascending).
    for price, size in diff.asks:
        update_order_list(book.asks, price, size, ascending=True)
