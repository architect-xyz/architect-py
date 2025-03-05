# generated by datamodel-codegen:
#   filename:  TickersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.TickersResponse import TickersResponse
from architect_py.grpc_client.request import RequestUnary


from enum import Enum
from typing import List, Optional

from msgspec import Struct


class SortTickersBy(str, Enum):
    VOLUME_DESC = 'VOLUME_DESC'
    CHANGE_ASC = 'CHANGE_ASC'
    CHANGE_DESC = 'CHANGE_DESC'
    ABS_CHANGE_DESC = 'ABS_CHANGE_DESC'


class TickersRequest(Struct):
    i: Optional[int] = None
    k: Optional[SortTickersBy] = None
    n: Optional[int] = None
    symbols: Optional[List[str]] = None
    venue: Optional[str] = None

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(TickersRequest, TickersResponse, "/json.architect.Marketdata/Tickers")

