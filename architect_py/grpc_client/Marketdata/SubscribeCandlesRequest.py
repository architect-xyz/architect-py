# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeCandlesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.Candle import Candle

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class SubscribeCandlesRequest(Struct):
    symbol: str
    candle_widths: Optional[
        Annotated[
            List[definitions.CandleWidth],
            Meta(description="If None, subscribe from all candle widths on the feed"),
        ]
    ] = None
    """
    If None, subscribe from all candle widths on the feed
    """
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


ResponseType = Candle
route = "/json.architect.Marketdata/SubscribeCandles"
unary_type = "stream"
