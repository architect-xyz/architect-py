# generated by datamodel-codegen:
#   filename:  Marketdata/HistoricalCandlesResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .Candle import Candle


class HistoricalCandlesResponse(Struct):
    candles: List[Candle]
