# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeManyCandlesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.Candle import Candle

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class SubscribeManyCandlesRequest(Struct, omit_defaults=True):
    candle_width: definitions.CandleWidth
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

    # below is a constructor that takes all field titles as arguments for convenience
    @staticmethod
    def new(
        candle_width: definitions.CandleWidth,
        symbols: Optional[List[str]] = None,
        venue: Optional[str] = None,
    ) -> "SubscribeManyCandlesRequest":
        return SubscribeManyCandlesRequest(
            candle_width,
            symbols,
            venue,
        )

    def __str__(self) -> str:
        return f"SubscribeManyCandlesRequest(candle_width={self.candle_width},symbols={self.symbols},venue={self.venue})"

    @staticmethod
    def get_response_type():
        return Candle

    @staticmethod
    def get_unannotated_response_type():
        return Candle

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Marketdata/SubscribeManyCandles"

    @staticmethod
    def get_rpc_method():
        return "stream"
