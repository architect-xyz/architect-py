# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeL2BookUpdatesRequest.json

from __future__ import annotations

from typing import Optional

from msgspec import Struct


class SubscribeL2BookUpdatesRequest(Struct):
    symbol: str
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return "&RESPONSE_TYPE:SubscribeL2BookUpdatesRequest"

    @staticmethod
    def get_route() -> str:
        return "&ROUTE:SubscribeL2BookUpdatesRequest"

    @staticmethod
    def get_unary_type():
        return "&UNARY_TYPE:SubscribeL2BookUpdatesRequest"
