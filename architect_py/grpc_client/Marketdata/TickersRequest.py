# generated by datamodel-codegen:
#   filename:  Marketdata/TickersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.TickersResponse import TickersResponse

from typing import List, Optional

from msgspec import Struct

from .. import definitions


class TickersRequest(Struct):
    i: Optional[int] = None
    k: Optional[definitions.SortTickersBy] = None
    n: Optional[int] = None
    symbols: Optional[List[str]] = None
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


ResponseType = TickersResponse
route = "/json.architect.Marketdata/Tickers"
unary_type = "unary"

