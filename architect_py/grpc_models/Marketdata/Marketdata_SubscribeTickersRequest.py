# generated by datamodel-codegen:
#   filename:  Marketdata_SubscribeTickersRequest.json

from __future__ import annotations

from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class SubscribeTickersRequest(Struct):
    symbols: Optional[
        Annotated[
            List[str],
            Meta(description='If None, subscribe from all symbols on the feed'),
        ]
    ] = None
