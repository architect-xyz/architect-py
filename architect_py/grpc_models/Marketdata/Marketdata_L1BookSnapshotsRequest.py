# generated by datamodel-codegen:
#   filename:  Marketdata_L1BookSnapshotsRequest.json

from __future__ import annotations

from typing import List, Optional

from msgspec import Struct


class L1BookSnapshotsRequest(Struct):
    symbols: Optional[List[str]] = None
