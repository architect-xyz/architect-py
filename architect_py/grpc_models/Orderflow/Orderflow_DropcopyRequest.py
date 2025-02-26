# generated by datamodel-codegen:
#   filename:  Orderflow_DropcopyRequest.json
#   timestamp: 2025-02-26T08:01:03+00:00

from __future__ import annotations

from msgspec import Struct


class DropcopyRequest(Struct):
    aberrant_fills: bool | None = False
    account: str | None = None
    execution_venue: str | None = None
    fills: bool | None = True
    orders: bool | None = False
    trader: str | None = None
