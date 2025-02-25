# generated by datamodel-codegen:
#   filename:  Oms_PendingCancelsRequest.json
#   timestamp: 2025-02-25T21:20:40+00:00

from __future__ import annotations

from typing import List

from msgspec import Struct


class PendingCancelsRequest(Struct):
    account: str | None = None
    cancel_ids: List[str] | None = None
    symbol: str | None = None
    trader: str | None = None
    venue: str | None = None
