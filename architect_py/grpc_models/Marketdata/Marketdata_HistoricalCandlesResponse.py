# generated by datamodel-codegen:
#   filename:  Marketdata_HistoricalCandlesResponse.json
#   timestamp: 2025-02-25T21:20:43+00:00

from __future__ import annotations

from enum import Enum
from typing import Annotated, List

from msgspec import Meta, Struct


class CandleWidth(Enum):
    integer_1 = 1
    integer_2 = 2
    integer_4 = 4
    integer_8 = 8
    integer_16 = 16
    integer_32 = 32


class Candle(Struct):
    av: Annotated[str, Meta(title='sell_volume')]
    bv: Annotated[str, Meta(title='buy_volume')]
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    v: Annotated[str, Meta(title='volume')]
    w: Annotated[CandleWidth, Meta(title='width')]
    ac: Annotated[str | None, Meta(title='ask_close')] | None = None
    ah: Annotated[str | None, Meta(title='ask_high')] | None = None
    al: Annotated[str | None, Meta(title='ask_low')] | None = None
    ao: Annotated[str | None, Meta(title='ask_open')] | None = None
    bc: Annotated[str | None, Meta(title='bid_close')] | None = None
    bh: Annotated[str | None, Meta(title='bid_high')] | None = None
    bl: Annotated[str | None, Meta(title='bid_low')] | None = None
    bo: Annotated[str | None, Meta(title='bid_open')] | None = None
    c: Annotated[str | None, Meta(title='close')] | None = None
    h: Annotated[str | None, Meta(title='high')] | None = None
    l: Annotated[str | None, Meta(title='low')] | None = None
    mc: Annotated[str | None, Meta(title='mid_close')] | None = None
    mh: Annotated[str | None, Meta(title='mid_high')] | None = None
    ml: Annotated[str | None, Meta(title='mid_low')] | None = None
    mo: Annotated[str | None, Meta(title='mid_open')] | None = None
    o: Annotated[str | None, Meta(title='open')] | None = None


class HistoricalCandlesResponse(Struct):
    candles: List[Candle]
