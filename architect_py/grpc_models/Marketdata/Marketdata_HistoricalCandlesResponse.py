# generated by datamodel-codegen:
#   filename:  Marketdata_HistoricalCandlesResponse.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class CandleWidth(int, Enum):
    integer_1 = 1
    integer_2 = 2
    integer_4 = 4
    integer_8 = 8
    integer_16 = 16
    integer_32 = 32


Decimal = str


class Candle(Struct):
    av: Annotated[Decimal, Meta(title='sell_volume')]
    bv: Annotated[Decimal, Meta(title='buy_volume')]
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    v: Annotated[Decimal, Meta(title='volume')]
    w: Annotated[CandleWidth, Meta(title='width')]
    ac: Optional[Annotated[Optional[Decimal], Meta(title='ask_close')]] = None
    ah: Optional[Annotated[Optional[Decimal], Meta(title='ask_high')]] = None
    al: Optional[Annotated[Optional[Decimal], Meta(title='ask_low')]] = None
    ao: Optional[Annotated[Optional[Decimal], Meta(title='ask_open')]] = None
    bc: Optional[Annotated[Optional[Decimal], Meta(title='bid_close')]] = None
    bh: Optional[Annotated[Optional[Decimal], Meta(title='bid_high')]] = None
    bl: Optional[Annotated[Optional[Decimal], Meta(title='bid_low')]] = None
    bo: Optional[Annotated[Optional[Decimal], Meta(title='bid_open')]] = None
    c: Optional[Annotated[Optional[Decimal], Meta(title='close')]] = None
    h: Optional[Annotated[Optional[Decimal], Meta(title='high')]] = None
    l: Optional[Annotated[Optional[Decimal], Meta(title='low')]] = None
    mc: Optional[Annotated[Optional[Decimal], Meta(title='mid_close')]] = None
    mh: Optional[Annotated[Optional[Decimal], Meta(title='mid_high')]] = None
    ml: Optional[Annotated[Optional[Decimal], Meta(title='mid_low')]] = None
    mo: Optional[Annotated[Optional[Decimal], Meta(title='mid_open')]] = None
    o: Optional[Annotated[Optional[Decimal], Meta(title='open')]] = None

    @property
    def sell_volume(self) -> Decimal:
        return self.av

    @sell_volume.setter
    def sell_volume(self, value: Decimal) -> None:
        self.av = value

    @property
    def buy_volume(self) -> Decimal:
        return self.bv

    @buy_volume.setter
    def buy_volume(self, value: Decimal) -> None:
        self.bv = value

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
    def volume(self) -> Decimal:
        return self.v

    @volume.setter
    def volume(self, value: Decimal) -> None:
        self.v = value

    @property
    def width(self) -> CandleWidth:
        return self.w

    @width.setter
    def width(self, value: CandleWidth) -> None:
        self.w = value

    @property
    def ask_close(self) -> Optional[Decimal]:
        return self.ac

    @ask_close.setter
    def ask_close(self, value: Optional[Decimal]) -> None:
        self.ac = value

    @property
    def ask_high(self) -> Optional[Decimal]:
        return self.ah

    @ask_high.setter
    def ask_high(self, value: Optional[Decimal]) -> None:
        self.ah = value

    @property
    def ask_low(self) -> Optional[Decimal]:
        return self.al

    @ask_low.setter
    def ask_low(self, value: Optional[Decimal]) -> None:
        self.al = value

    @property
    def ask_open(self) -> Optional[Decimal]:
        return self.ao

    @ask_open.setter
    def ask_open(self, value: Optional[Decimal]) -> None:
        self.ao = value

    @property
    def bid_close(self) -> Optional[Decimal]:
        return self.bc

    @bid_close.setter
    def bid_close(self, value: Optional[Decimal]) -> None:
        self.bc = value

    @property
    def bid_high(self) -> Optional[Decimal]:
        return self.bh

    @bid_high.setter
    def bid_high(self, value: Optional[Decimal]) -> None:
        self.bh = value

    @property
    def bid_low(self) -> Optional[Decimal]:
        return self.bl

    @bid_low.setter
    def bid_low(self, value: Optional[Decimal]) -> None:
        self.bl = value

    @property
    def bid_open(self) -> Optional[Decimal]:
        return self.bo

    @bid_open.setter
    def bid_open(self, value: Optional[Decimal]) -> None:
        self.bo = value

    @property
    def close(self) -> Optional[Decimal]:
        return self.c

    @close.setter
    def close(self, value: Optional[Decimal]) -> None:
        self.c = value

    @property
    def high(self) -> Optional[Decimal]:
        return self.h

    @high.setter
    def high(self, value: Optional[Decimal]) -> None:
        self.h = value

    @property
    def low(self) -> Optional[Decimal]:
        return self.l

    @low.setter
    def low(self, value: Optional[Decimal]) -> None:
        self.l = value

    @property
    def mid_close(self) -> Optional[Decimal]:
        return self.mc

    @mid_close.setter
    def mid_close(self, value: Optional[Decimal]) -> None:
        self.mc = value

    @property
    def mid_high(self) -> Optional[Decimal]:
        return self.mh

    @mid_high.setter
    def mid_high(self, value: Optional[Decimal]) -> None:
        self.mh = value

    @property
    def mid_low(self) -> Optional[Decimal]:
        return self.ml

    @mid_low.setter
    def mid_low(self, value: Optional[Decimal]) -> None:
        self.ml = value

    @property
    def mid_open(self) -> Optional[Decimal]:
        return self.mo

    @mid_open.setter
    def mid_open(self, value: Optional[Decimal]) -> None:
        self.mo = value

    @property
    def open(self) -> Optional[Decimal]:
        return self.o

    @open.setter
    def open(self, value: Optional[Decimal]) -> None:
        self.o = value


class HistoricalCandlesResponse(Struct):
    candles: List[Candle]
