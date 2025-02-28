# generated by datamodel-codegen:
#   filename:  Marketdata_SubscribeCurrentCandlesRequest.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional

from msgspec import Meta, Struct


class CandleWidth(int, Enum):
    integer_1 = 1
    integer_2 = 2
    integer_4 = 4
    integer_8 = 8
    integer_16 = 16
    integer_32 = 32


class SubscribeCurrentCandlesRequest(Struct):
    candle_width: CandleWidth
    symbol: str
    tick_period_ms: Optional[
        Annotated[
            Optional[int],
            Meta(
                description='If None, send the current candle on every trade or candle tick. Otherwise, send a candle every `tick_period_ms`.',
                ge=0,
            ),
        ]
    ] = None
    venue: Optional[str] = None
