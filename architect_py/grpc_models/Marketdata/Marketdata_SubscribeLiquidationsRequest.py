# generated by datamodel-codegen:
#   filename:  Marketdata_SubscribeLiquidationsRequest.json

from __future__ import annotations

from typing import List, Optional

from msgspec import Struct


class SubscribeLiquidationsRequest(Struct):
    symbols: Optional[List[str]] = None
