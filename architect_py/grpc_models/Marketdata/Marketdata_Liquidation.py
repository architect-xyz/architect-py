from decimal import Decimal

# generated by datamodel-codegen:
#   filename:  Marketdata_Liquidation.json

from __future__ import annotations

from enum import Enum
from typing import Annotated

from msgspec import Meta, Struct



class Dir(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class Liquidation(Struct):
    d: Annotated[Dir, Meta(title='direction')]
    p: Annotated[Decimal, Meta(title='price')]
    q: Annotated[Decimal, Meta(title='size')]
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]

    @property
    def direction(self) -> Dir:
        return self.d

    @direction.setter
    def direction(self, value: Dir) -> None:
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
