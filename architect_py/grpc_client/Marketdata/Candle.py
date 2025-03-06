# generated by datamodel-codegen:
#   filename:  Marketdata/Candle.json

from __future__ import annotations
from datetime import datetime, timezone

from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class Candle(Struct):
    av: Annotated[definitions.DecimalModel, Meta(title='sell_volume')]
    bv: Annotated[definitions.DecimalModel, Meta(title='buy_volume')]
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    v: Annotated[definitions.DecimalModel, Meta(title='volume')]
    w: Annotated[definitions.CandleWidth, Meta(title='width')]
    ac: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='ask_close')]
    ] = None
    ah: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='ask_high')]
    ] = None
    al: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='ask_low')]
    ] = None
    ao: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='ask_open')]
    ] = None
    bc: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='bid_close')]
    ] = None
    bh: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='bid_high')]
    ] = None
    bl: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='bid_low')]
    ] = None
    bo: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='bid_open')]
    ] = None
    c: Optional[Annotated[Optional[definitions.DecimalModel], Meta(title='close')]] = (
        None
    )
    h: Optional[Annotated[Optional[definitions.DecimalModel], Meta(title='high')]] = (
        None
    )
    l: Optional[Annotated[Optional[definitions.DecimalModel], Meta(title='low')]] = None
    mc: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='mid_close')]
    ] = None
    mh: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='mid_high')]
    ] = None
    ml: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='mid_low')]
    ] = None
    mo: Optional[
        Annotated[Optional[definitions.DecimalModel], Meta(title='mid_open')]
    ] = None
    o: Optional[Annotated[Optional[definitions.DecimalModel], Meta(title='open')]] = (
        None
    )

    @property
    def sell_volume(self) -> definitions.DecimalModel:
        return self.av

    @sell_volume.setter
    def sell_volume(self, value: definitions.DecimalModel) -> None:
        self.av = value

    @property
    def buy_volume(self) -> definitions.DecimalModel:
        return self.bv

    @buy_volume.setter
    def buy_volume(self, value: definitions.DecimalModel) -> None:
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
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.ts, tz=timezone.utc)

    @property
    def datetime_local(self) -> datetime:
        return datetime.fromtimestamp(self.ts)

    @property
    def volume(self) -> definitions.DecimalModel:
        return self.v

    @volume.setter
    def volume(self, value: definitions.DecimalModel) -> None:
        self.v = value

    @property
    def width(self) -> definitions.CandleWidth:
        return self.w

    @width.setter
    def width(self, value: definitions.CandleWidth) -> None:
        self.w = value

    @property
    def ask_close(self) -> Optional[definitions.DecimalModel]:
        return self.ac

    @ask_close.setter
    def ask_close(self, value: Optional[definitions.DecimalModel]) -> None:
        self.ac = value

    @property
    def ask_high(self) -> Optional[definitions.DecimalModel]:
        return self.ah

    @ask_high.setter
    def ask_high(self, value: Optional[definitions.DecimalModel]) -> None:
        self.ah = value

    @property
    def ask_low(self) -> Optional[definitions.DecimalModel]:
        return self.al

    @ask_low.setter
    def ask_low(self, value: Optional[definitions.DecimalModel]) -> None:
        self.al = value

    @property
    def ask_open(self) -> Optional[definitions.DecimalModel]:
        return self.ao

    @ask_open.setter
    def ask_open(self, value: Optional[definitions.DecimalModel]) -> None:
        self.ao = value

    @property
    def bid_close(self) -> Optional[definitions.DecimalModel]:
        return self.bc

    @bid_close.setter
    def bid_close(self, value: Optional[definitions.DecimalModel]) -> None:
        self.bc = value

    @property
    def bid_high(self) -> Optional[definitions.DecimalModel]:
        return self.bh

    @bid_high.setter
    def bid_high(self, value: Optional[definitions.DecimalModel]) -> None:
        self.bh = value

    @property
    def bid_low(self) -> Optional[definitions.DecimalModel]:
        return self.bl

    @bid_low.setter
    def bid_low(self, value: Optional[definitions.DecimalModel]) -> None:
        self.bl = value

    @property
    def bid_open(self) -> Optional[definitions.DecimalModel]:
        return self.bo

    @bid_open.setter
    def bid_open(self, value: Optional[definitions.DecimalModel]) -> None:
        self.bo = value

    @property
    def close(self) -> Optional[definitions.DecimalModel]:
        return self.c

    @close.setter
    def close(self, value: Optional[definitions.DecimalModel]) -> None:
        self.c = value

    @property
    def high(self) -> Optional[definitions.DecimalModel]:
        return self.h

    @high.setter
    def high(self, value: Optional[definitions.DecimalModel]) -> None:
        self.h = value

    @property
    def low(self) -> Optional[definitions.DecimalModel]:
        return self.l

    @low.setter
    def low(self, value: Optional[definitions.DecimalModel]) -> None:
        self.l = value

    @property
    def mid_close(self) -> Optional[definitions.DecimalModel]:
        return self.mc

    @mid_close.setter
    def mid_close(self, value: Optional[definitions.DecimalModel]) -> None:
        self.mc = value

    @property
    def mid_high(self) -> Optional[definitions.DecimalModel]:
        return self.mh

    @mid_high.setter
    def mid_high(self, value: Optional[definitions.DecimalModel]) -> None:
        self.mh = value

    @property
    def mid_low(self) -> Optional[definitions.DecimalModel]:
        return self.ml

    @mid_low.setter
    def mid_low(self, value: Optional[definitions.DecimalModel]) -> None:
        self.ml = value

    @property
    def mid_open(self) -> Optional[definitions.DecimalModel]:
        return self.mo

    @mid_open.setter
    def mid_open(self, value: Optional[definitions.DecimalModel]) -> None:
        self.mo = value

    @property
    def open(self) -> Optional[definitions.DecimalModel]:
        return self.o

    @open.setter
    def open(self, value: Optional[definitions.DecimalModel]) -> None:
        self.o = value
