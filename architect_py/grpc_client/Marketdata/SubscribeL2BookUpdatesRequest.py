# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeL2BookUpdatesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.L2BookUpdate import (
    L2BookUpdate,
    Snapshot,
    Diff,
)

from typing import Optional

from msgspec import Struct


class SubscribeL2BookUpdatesRequest(Struct, omit_defaults=True):
    symbol: str
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return L2BookUpdate

    @staticmethod
    def get_unannotated_response_type():
        return Snapshot | Diff

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Marketdata/SubscribeL2BookUpdates"

    @staticmethod
    def get_rpc_method():
        return "stream"
