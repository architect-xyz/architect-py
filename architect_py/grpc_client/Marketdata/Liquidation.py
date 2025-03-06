# generated by datamodel-codegen:
#   filename:  Marketdata/Liquidation.json

from __future__ import annotations
from datetime import datetime, timezone

from typing import Annotated

from msgspec import Meta, Struct

from .. import definitions


class Price(Struct):
    pass


class Size(Struct):
    pass


class Liquidation(Struct):
    d: Annotated[definitions.Dir, Meta(title='direction')]
    p: Annotated[Price, Meta(title='price')]
    q: Annotated[Size, Meta(title='size')]
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]

    @property
    def direction(self) -> definitions.Dir:
        return self.d

    @direction.setter
    def direction(self, value: definitions.Dir) -> None:
        self.d = value

    @property
    def price(self) -> Price:
        return self.p

    @price.setter
    def price(self, value: Price) -> None:
        self.p = value

    @property
    def size(self) -> Size:
        return self.q

    @size.setter
    def size(self, value: Size) -> None:
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
