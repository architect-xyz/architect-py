# generated by datamodel-codegen:
#   filename:  Marketdata_SubscribeTradesRequest.json

from __future__ import annotations

from typing import Annotated, Optional

from msgspec import Meta, Struct


class SubscribeTradesRequest(Struct):
    symbol: Optional[
        Annotated[
            Optional[str],
            Meta(description='If None, subscribe from all symbols on the feed'),
        ]
    ] = None
    venue: Optional[str] = None
