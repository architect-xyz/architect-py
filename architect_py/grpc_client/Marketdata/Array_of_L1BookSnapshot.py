# generated by datamodel-codegen:
#   filename:  Array_of_L1BookSnapshot.json

from __future__ import annotations
from datetime import datetime, timezone

from decimal import Decimal
from typing import Annotated, List, Optional

from msgspec import Meta, Struct

DecimalModel = Decimal


class L1BookSnapshot(Struct):
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    a: Optional[Annotated[List[Decimal], Meta(title='best_ask')]] = None
    b: Optional[Annotated[List[Decimal], Meta(title='best_bid')]] = None

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
    def best_ask(self) -> Optional[List[Decimal]]:
        return self.a

    @best_ask.setter
    def best_ask(self, value: Optional[List[Decimal]]) -> None:
        self.a = value

    @property
    def best_bid(self) -> Optional[List[Decimal]]:
        return self.b

    @best_bid.setter
    def best_bid(self, value: Optional[List[Decimal]]) -> None:
        self.b = value


ArrayOfL1BookSnapshot = Annotated[
    List[L1BookSnapshot], Meta(title='Array_of_L1BookSnapshot')
]
