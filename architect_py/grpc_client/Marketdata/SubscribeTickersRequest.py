# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeTickersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.TickerUpdate import TickerUpdate

from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class SubscribeTickersRequest(Struct):
    """
    Ticker updates are not strongly ordered because the data is considered more casual.  You may receive diffs or snapshots slightly out of order.
    """

    symbols: Optional[
        Annotated[
            List[str],
            Meta(description='If None, subscribe from all symbols on the feed'),
        ]
    ] = None
    """
    If None, subscribe from all symbols on the feed
    """

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


ResponseType = TickerUpdate
route = "/json.architect.Marketdata/SubscribeTickers"
unary_type = "stream"

