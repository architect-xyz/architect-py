import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal, Optional, Union
from uuid import UUID

import grpc
import msgspec

from architect_py.graphql_client.subscribe_trades import SubscribeTradesTrades
from architect_py.scalars import OrderDir


class JsonMarketdataStub:
    def __init__(self, channel: Union[grpc.Channel, grpc.aio.Channel]):
        self.SubscribeL1BookSnapshots = channel.unary_stream(
            "/json.architect.Marketdata/SubscribeL1BookSnapshots",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L1BookSnapshot
            ),
        )
        self.L2BookSnapshot = channel.unary_unary(
            "/json.architect.Marketdata/L2BookSnapshot",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L2BookSnapshot
            ),
        )
        self.SubscribeL2BookUpdates = channel.unary_stream(
            "/json.architect.Marketdata/SubscribeL2BookUpdates",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L2BookUpdate
            ),
        )


class SubscribeL1BookSnapshotsRequest(msgspec.Struct, kw_only=True):
    market_ids: list[str] | None


class L1BookSnapshot(msgspec.Struct, kw_only=True):
    market_id: UUID = msgspec.field(name="m")
    timestamp_s: int = msgspec.field(name="ts")
    timestamp_ns: int = msgspec.field(name="tn")
    epoch: int | None = msgspec.field(name="e", default=None)
    seqno: int | None = msgspec.field(name="n", default=None)
    best_bid: tuple[Decimal, Decimal] | None = msgspec.field(name="b")
    best_ask: tuple[Decimal, Decimal] | None = msgspec.field(name="a")

    def timestamp(self):
        dt = datetime.fromtimestamp(self.timestamp_s)
        return dt.replace(microsecond=self.timestamp_ns // 1000)


class L2BookSnapshotRequest(msgspec.Struct, kw_only=True):
    market_id: str


class SubscribeL2BookUpdatesRequest(msgspec.Struct, kw_only=True):
    market_id: str


class L2BookSnapshot(msgspec.Struct, kw_only=True, tag_field="t", tag="s"):
    timestamp_s: int = msgspec.field(name="ts")
    timestamp_ns: int = msgspec.field(name="tn")
    sequence_id: int = msgspec.field(name="sid")
    sequence_number: int = msgspec.field(name="sn")
    bids: list[tuple[Decimal, Decimal]] = msgspec.field(name="b")
    asks: list[tuple[Decimal, Decimal]] = msgspec.field(name="a")

    def timestamp(self):
        dt = datetime.fromtimestamp(self.timestamp_s)
        return dt.replace(microsecond=self.timestamp_ns // 1000)


class L2BookDiff(msgspec.Struct, kw_only=True, tag_field="t", tag="d"):
    timestamp_s: int = msgspec.field(name="ts")
    timestamp_ns: int = msgspec.field(name="tn")
    sequence_id: int = msgspec.field(name="sid")
    sequence_number: int = msgspec.field(name="sn")
    # Set of (price, size) updates. If zero, the price level
    # has been removed from the book.
    bids: list[tuple[Decimal, Decimal]] = msgspec.field(name="b")
    # Set of (price, size) updates. If zero, the price level
    # has been removed from the book.
    asks: list[tuple[Decimal, Decimal]] = msgspec.field(name="a")

    def timestamp(self):
        dt = datetime.fromtimestamp(self.timestamp_s)
        return dt.replace(microsecond=self.timestamp_ns // 1000)


L2BookUpdate = Union[L2BookSnapshot, L2BookDiff]


@dataclass(kw_only=True)
class QueryL2BookSnapshot:
    market_id: uuid.UUID


@dataclass(kw_only=True)
class ExternalL2BookSnapshot:
    timestamp: datetime
    epoch: datetime
    seqno: int
    bids: list[tuple[Decimal, Decimal]]
    asks: list[tuple[Decimal, Decimal]]


@dataclass(kw_only=True)
class QueryL3BookSnapshot:
    market_id: uuid.UUID


@dataclass(kw_only=True)
class L3Order:
    price: Decimal
    size: Decimal

    def __init__(self, *, price: Decimal, size: Decimal, **kwargs):
        self.price = price
        self.size = size
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass(kw_only=True)
class L3BookSnapshot:
    timestamp: datetime
    epoch: datetime
    seqno: int
    bids: list[L3Order]
    asks: list[L3Order]

    @staticmethod
    def from_dict(d) -> "L3BookSnapshot":
        return L3BookSnapshot(
            timestamp=d["timestamp"],
            epoch=d["epoch"],
            seqno=d["seqno"],
            bids=[L3Order(**b) for b in d["bids"]],
            asks=[L3Order(**a) for a in d["asks"]],
        )


@dataclass(kw_only=True)
class CandleV1:
    time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    buy_volume: Decimal
    sell_volume: Decimal


@dataclass(kw_only=True)
class TradeV1(SubscribeTradesTrades):
    def __init__(
        self,
        *,
        time: Optional[datetime],
        direction: Optional[Literal["Buy", "Sell"]],
        price: Decimal,
        size: Decimal,
        **kwargs
    ):
        self.time = time
        self.direction = OrderDir.from_string(direction) if direction else None
        self.price = price
        self.size = size
        for k, v in kwargs.items():
            setattr(self, k, v)
