# generated by datamodel-codegen:
#   filename:  Marketdata/TickersResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from . import Ticker


class TickersResponse(Struct):
    tickers: List[Ticker]
