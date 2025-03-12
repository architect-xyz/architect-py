# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeCurrentCandlesRequest.json

from __future__ import annotations

from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class SubscribeCurrentCandlesRequest(Struct):
    """
    Subscribe to the current candle.  This allows you to display the most recent/building candle live in a UI, for example.
    """

    candle_width: definitions.CandleWidth
    symbol: str
    tick_period_ms: Optional[
        Annotated[
            Optional[int],
            Meta(
                description='If None, send the current candle on every trade or candle tick. Otherwise, send a candle every `tick_period_ms`.',
                ge=0,
            ),
        ]
    ] = None
    """
    If None, send the current candle on every trade or candle tick. Otherwise, send a candle every `tick_period_ms`.
    """
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return "&RESPONSE_TYPE:SubscribeCurrentCandlesRequest"

    @staticmethod
    def get_route() -> str:
        return "&ROUTE:SubscribeCurrentCandlesRequest"

    @staticmethod
    def get_unary_type():
        return "&UNARY_TYPE:SubscribeCurrentCandlesRequest"
