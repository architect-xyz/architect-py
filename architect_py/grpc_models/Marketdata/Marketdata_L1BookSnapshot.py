# generated by datamodel-codegen:
#   filename:  Marketdata_L1BookSnapshot.json
#   timestamp: 2025-02-25T21:20:43+00:00

from __future__ import annotations

from typing import Annotated, List

from msgspec import Meta, Struct

Decimal = str


class L1BookSnapshot(Struct):
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    a: Annotated[List[Decimal | str], Meta(title='best_ask')] | None = None
    b: Annotated[List[Decimal | str], Meta(title='best_bid')] | None = None
