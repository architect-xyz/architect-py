# generated by datamodel-codegen:
#   filename:  Marketdata/Trade.json

from __future__ import annotations
from architect_py.scalars import OrderDir
from datetime import datetime, timezone

from decimal import Decimal
from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class Trade(Struct):
    p: Annotated[Decimal, Meta(title="price")]
    q: Annotated[Decimal, Meta(title="size")]
    s: Annotated[str, Meta(title="symbol")]
    tn: Annotated[int, Meta(ge=0, title="timestamp_ns")]
    ts: Annotated[int, Meta(title="timestamp")]
    d: Optional[Annotated[Optional[OrderDir], Meta(title="direction")]] = None

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

    @property
    def direction(self) -> Optional[OrderDir]:
        return self.d

    @direction.setter
    def direction(self, value: Optional[OrderDir]) -> None:
        self.d = value
