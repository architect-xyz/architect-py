# generated by datamodel-codegen:
#   filename:  Marketdata/TickerUpdate.json

from __future__ import annotations

from typing import Annotated

from msgspec import Meta

from . import Ticker

TickerUpdate = Annotated[Ticker, Meta(title='TickerUpdate')]
