# generated by datamodel-codegen:
#   filename:  Marketdata_L1BookSnapshotRequest.json
#   timestamp: 2025-02-25T21:20:45+00:00

from __future__ import annotations

from msgspec import Struct


class L1BookSnapshotRequest(Struct):
    symbol: str
