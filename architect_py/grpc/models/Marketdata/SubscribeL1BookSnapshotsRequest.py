# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeL1BookSnapshotsRequest.json

from __future__ import annotations
from architect_py.grpc.models.Marketdata.L1BookSnapshot import L1BookSnapshot

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
    venue: Optional[str] = None

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        symbols: Optional[List[str]] = None,
        venue: Optional[str] = None,
    ):
        return cls(
            symbols,
            venue,
        )

    def __str__(self) -> str:
        return f"SubscribeL1BookSnapshotsRequest(symbols={self.symbols},venue={self.venue})"

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
    def get_rpc_method():
        return "stream"
