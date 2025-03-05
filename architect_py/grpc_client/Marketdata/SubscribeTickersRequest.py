# generated by datamodel-codegen:
#   filename:  SubscribeTickersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.TickerUpdate import TickerUpdate
from architect_py.grpc_client.request import RequestStream


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
    def get_request_helper():
        return request_helper


request_helper = RequestStream(SubscribeTickersRequest, typing.Union[TickerUpdate.TickerUpdate1, TickerUpdate.TickerUpdate2], "/json.architect.Marketdata/SubscribeTickers")

