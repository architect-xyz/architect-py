# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeTradesRequest.json

from __future__ import annotations
from architect_py.grpc.models.Marketdata.Trade import Trade

from typing import Annotated, Optional

from msgspec import Meta, Struct


class SubscribeTradesRequest(Struct, omit_defaults=True):
    symbol: Optional[
        Annotated[
            Optional[str],
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
        symbol: Optional[str] = None,
        venue: Optional[str] = None,
    ):
        return cls(
            symbol,
            venue,
        )

    def __str__(self) -> str:
        return f"SubscribeTradesRequest(symbol={self.symbol},venue={self.venue})"

    @staticmethod
    def get_response_type():
        return Trade

    @staticmethod
    def get_unannotated_response_type():
        return Trade

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Marketdata/SubscribeTrades"

    @staticmethod
    def get_rpc_method():
        return "stream"
