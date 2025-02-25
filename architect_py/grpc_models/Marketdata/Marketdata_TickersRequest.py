# generated by datamodel-codegen:
#   filename:  Marketdata_TickersRequest.json
#   timestamp: 2025-02-25T21:20:49+00:00

from __future__ import annotations

from enum import Enum
from typing import List

from msgspec import Struct


class SortTickersBy(Enum):
    VOLUME_DESC = 'VOLUME_DESC'
    CHANGE_ASC = 'CHANGE_ASC'
    CHANGE_DESC = 'CHANGE_DESC'
    ABS_CHANGE_DESC = 'ABS_CHANGE_DESC'


class TickersRequest(Struct):
    i: int | None = None
    k: SortTickersBy | None = None
    n: int | None = None
    symbols: List[str] | None = None
    venue: str | None = None
