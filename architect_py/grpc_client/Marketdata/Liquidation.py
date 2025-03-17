# generated by datamodel-codegen:
#   filename:  Marketdata/Liquidation.json

from __future__ import annotations
from architect_py.scalars import OrderDir
from datetime import datetime, timezone

from decimal import Decimal
from typing import Annotated

from msgspec import Meta, Struct

from .. import definitions


class Liquidation(Struct, omit_defaults=True):
    d: Annotated[OrderDir, Meta(title="direction")]
    p: Annotated[Decimal, Meta(title="price")]
    q: Annotated[Decimal, Meta(title="size")]
    s: Annotated[str, Meta(title="symbol")]
    tn: Annotated[int, Meta(ge=0, title="timestamp_ns")]
    ts: Annotated[int, Meta(title="timestamp")]

    # below is a constructor that takes all field titles as arguments for convenience
    @staticmethod
    def new(
        direction: OrderDir,
        price: Decimal,
        size: Decimal,
        symbol: str,
        timestamp_ns: int,
        timestamp: int,
    ) -> "Liquidation":
        return Liquidation(
            direction,
            price,
            size,
            symbol,
            timestamp_ns,
            timestamp,
        )

    def __str__(self) -> str:
        return f"Liquidation(direction={self.d},price={self.p},size={self.q},symbol={self.s},timestamp_ns={self.tn},timestamp={self.ts})"

    @property
    def direction(self) -> OrderDir:
        return self.d

    @direction.setter
    def direction(self, value: OrderDir) -> None:
        self.d = value

    @property
    def price(self) -> Decimal:
        return self.p

    @price.setter
    def price(self, value: Decimal) -> None:
        self.p = value

    @property
    def size(self) -> Decimal:
        return self.q

    @size.setter
    def size(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

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
        return datetime.fromtimestamp(self.ts, tz=timezone.utc)

    @property
    def datetime_local(self) -> datetime:
        return datetime.fromtimestamp(self.ts)
