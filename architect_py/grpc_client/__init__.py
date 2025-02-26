from asyncio.log import logger
from typing import Any, AsyncIterator, Optional, cast
from datetime import datetime, timedelta
from urllib.parse import urlparse


import dns.asyncresolver
import dns.resolver
from dns.rdtypes.IN.SRV import SRV

import grpc
import orjson
import websockets.client

from architect_py.graphql_client.client import GraphQLClient


from architect_py.grpc_models.Marketdata.Marketdata_Array_of_L1BookSnapshot import (
    L1BookSnapshot,
)
from architect_py.grpc_models.Marketdata.Marketdata_L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_models.Marketdata.Marketdata_L2BookSnapshotRequest import (
    L2BookSnapshotRequest,
)
from architect_py.grpc_models.Marketdata.Marketdata_L2BookUpdate import (
    Diff,
    L2BookUpdate,
    Snapshot,
)
from architect_py.grpc_models.Marketdata.Marketdata_SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from architect_py.grpc_models.Marketdata.Marketdata_SubscribeL2BookUpdatesRequest import (
    SubscribeL2BookUpdatesRequest,
)
from architect_py.grpc_models.Marketdata.Marketdata_Trade import Trade
from architect_py.protocol import (
    ProtocolQueryMessage,
    ProtocolResponseMessage,
    ProtocolSubscribeMessage,
)
from architect_py.protocol.marketdata import JsonMarketdataStub

from architect_py.scalars import TradableProduct
from architect_py.utils.grpc_root_certificates import grpc_root_certificates


# TODO:
# FIX decimal.Decimal in the generated code
# make field titles take the main name
# Fix the duplication issue in the generated code


class GRPCClient:
    def __init__(self, graphql_client: GraphQLClient):
        self.grpc_jwt: Optional[str] = None
        self.grpc_jwt_expiration: Optional[datetime] = None
        self.grpc_root_certificates = grpc_root_certificates
        self.graphql_client = graphql_client

        self.marketdata: dict[str, JsonWsClient] = {}  # cpty => JsonWsClient
        self.l2_books: dict[TradableProduct, Snapshot] = {}

    async def grpc_channel(self, endpoint: str):
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
                root_certificates=self.grpc_root_certificates
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
            or self.grpc_jwt is None
            or (
                self.grpc_jwt_expiration is not None
                and datetime.now() > self.grpc_jwt_expiration - timedelta(minutes=1)
            )
        ):
            try:
                self.grpc_jwt = (await self.graphql_client.create_jwt()).create_jwt
                self.grpc_jwt_expiration = datetime.now() + timedelta(hours=23)
            except Exception as e:
                logger.error("Failed to refresh gRPC credentials: %s", e)

        return self.grpc_jwt

    def configure_marketdata(self, *, cpty: str, url: str):
        self.marketdata[cpty] = JsonWsClient(url=url)

    async def l2_book_snapshot(
        self, endpoint: str, venue: Optional[str], symbol: str
    ) -> L2BookSnapshot:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = L2BookSnapshotRequest(venue=venue, symbol=symbol)
        jwt = await self.refresh_grpc_credentials()
        return await stub.L2BookSnapshot(
            req, metadata=(("authorization", f"Bearer {jwt}"),)
        )

    async def subscribe_l1_book_snapshots(
        self, endpoint: str, symbols: list[str] | None = None
    ) -> AsyncIterator[L1BookSnapshot]:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = SubscribeL1BookSnapshotsRequest(symbols=symbols)
        call = stub.SubscribeL1BookSnapshots(req)
        async for snapshot in call:
            yield snapshot

    async def subscribe_l2_book_updates(
        self,
        endpoint: str,
        symbol: TradableProduct,
        venue: Optional[str],
    ) -> AsyncIterator[L2BookUpdate]:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = SubscribeL2BookUpdatesRequest(venue=venue, symbol=symbol)
        jwt = await self.refresh_grpc_credentials()
        call = stub.SubscribeL2BookUpdates(
            req, metadata=(("authorization", f"Bearer {jwt}"),)
        )
        async for snapshot in call:
            yield snapshot

    async def watch_l2_book(
        self, endpoint: str, symbol: TradableProduct, venue: Optional[str]
    ) -> AsyncIterator[tuple[int, int]]:
        async for up in self.subscribe_l2_book_updates(
            endpoint, symbol=symbol, venue=venue
        ):
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
                book.update_from_diff(up)

            yield (up.sequence_id, up.sequence_number)

    async def subscribe_trades(self, symbol: str, venue: str) -> AsyncIterator[Trade]:
        client = self.marketdata.get(venue)
        if client is None:
            raise ValueError(f"no marketdata client configured for {venue}")
        return client.subscribe_trades(symbol)


def L2_update_from_diff(book: L2BookSnapshot, diff: L2BookUpdate):
    book.timestamp_s = diff.timestamp_s
    book.timestamp_ns = diff.timestamp_ns
    book.sequence_id = diff.sequence_id
    book.sequence_number = diff.sequence_number
    for price, size in diff.bids:
        if size.is_zero():
            if price in book.bids:
                del book.bids[price]
        else:
            book.bids[price] = size
    for price, size in diff.asks:
        if size.is_zero():
            if price in book.asks:
                del book.asks[price]
        else:
            book.asks[price] = size


class JsonWsClient:
    def __init__(self, *, url: str):
        self.url = url
        self.next_request_id = 1

    def _connect(self):
        return websockets.client.connect(self.url, max_size=1_000_000_000)

    def _request_id(self):
        request_id = self.next_request_id
        self.next_request_id += 1
        return request_id

    async def request(self, method: str, params: Optional[Any] = None) -> Any:
        async with self._connect() as ws:
            id = self._request_id()
            query = ProtocolQueryMessage(
                id=id,
                type="query",
                method=method,
                params=params,
            )
            await ws.send(orjson.dumps(query))
            async for message in ws:
                m = orjson.loads(message)
                if m["type"] == "response":
                    res = ProtocolResponseMessage(**m)
                    if res.id == id:
                        if res.error:
                            raise Exception(res.error)
                        return res.result

    async def subscribe(self, topic: str) -> AsyncIterator[Any]:
        async with self._connect() as ws:
            id = self._request_id()
            query = ProtocolSubscribeMessage(
                id=id,
                type="subscribe",
                topic=topic,
            )
            await ws.send(orjson.dumps(query))
            async for message in ws:
                m = orjson.loads(message)
                if m["type"] == "update" and m["id"] == id:
                    yield m["data"]
                elif m["type"] == "response" and m["id"] == id:
                    if "error" in m:
                        raise Exception(m["error"])

    async def subscribe_trades(self, symbol: str) -> AsyncIterator[Trade]:
        async for data in self.subscribe(f"marketdata/trades/{symbol}"):
            yield Trade(**data)
