# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeL1BookSnapshotsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.L1BookSnapshot import L1BookSnapshot

from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class SubscribeL1BookSnapshotsRequest(Struct, omit_defaults=True):
    symbols: Optional[
        Annotated[
            List[str],
            Meta(description="If None, subscribe from all symbols on the feed"),
        ]
    ] = None
    """
    If None, subscribe from all symbols on the feed
    """

    @staticmethod
    def get_response_type():
        return L1BookSnapshot

    @staticmethod
    def get_unannotated_response_type():
        return L1BookSnapshot

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Marketdata/SubscribeL1BookSnapshots"

    @staticmethod
    def get_unary_type():
        return "stream"
