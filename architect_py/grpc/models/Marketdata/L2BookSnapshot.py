# generated by datamodel-codegen:
#   filename:  Marketdata/L2BookSnapshot.json

from __future__ import annotations
from datetime import datetime, timezone

from decimal import Decimal
from typing import Annotated, List

from msgspec import Meta, Struct

Ask = List[Decimal]


Bid = List[Decimal]


class L2BookSnapshot(Struct, omit_defaults=True):
    """
    Unique sequence id and number.
    """

    a: Annotated[List[Ask], Meta(title="asks")]
    b: Annotated[List[Bid], Meta(title="bids")]
    sid: Annotated[int, Meta(ge=0, title="sequence_id")]
    sn: Annotated[int, Meta(ge=0, title="sequence_number")]
    tn: Annotated[int, Meta(ge=0, title="timestamp_ns")]
    ts: Annotated[int, Meta(title="timestamp")]

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        asks: List[Ask],
        bids: List[Bid],
        sequence_id: int,
        sequence_number: int,
        timestamp_ns: int,
        timestamp: int,
    ):
        return cls(
            asks,
            bids,
            sequence_id,
            sequence_number,
            timestamp_ns,
            timestamp,
        )

    def __str__(self) -> str:
        return f"L2BookSnapshot(asks={self.a},bids={self.b},sequence_id={self.sid},sequence_number={self.sn},timestamp_ns={self.tn},timestamp={self.ts})"

    @property
    def asks(self) -> List[Ask]:
        return self.a

    @asks.setter
    def asks(self, value: List[Ask]) -> None:
        self.a = value

    @property
    def bids(self) -> List[Bid]:
        return self.b

    @bids.setter
    def bids(self, value: List[Bid]) -> None:
        self.b = value

    @property
    def sequence_id(self) -> int:
        return self.sid

    @sequence_id.setter
    def sequence_id(self, value: int) -> None:
        self.sid = value

    @property
    def sequence_number(self) -> int:
        return self.sn

    @sequence_number.setter
    def sequence_number(self, value: int) -> None:
        self.sn = value

    @property
    def timestamp_ns(self) -> int:
        return self.tn

    @timestamp_ns.setter
    def timestamp_ns(self, value: int) -> None:
        self.tn = value

    @property
    def timestamp(self) -> int:
        return self.ts

    @timestamp.setter
    def timestamp(self, value: int) -> None:
        self.ts = value

    @property
    def datetime(self) -> datetime:
        """
        Convenience property to get the timestamp as a datetime object in UTC.
        """
        return datetime.fromtimestamp(self.ts, tz=timezone.utc)

    @property
    def datetime_local(self) -> datetime:
        """
        Convenience property to get the timestamp as a datetime object in local time.
        """
        return datetime.fromtimestamp(self.ts)
