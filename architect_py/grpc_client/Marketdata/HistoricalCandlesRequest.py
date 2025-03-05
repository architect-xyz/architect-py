# generated by datamodel-codegen:
#   filename:  Marketdata/HistoricalCandlesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.HistoricalCandlesResponse import HistoricalCandlesResponse
from architect_py.grpc_client.request import RequestUnary


from enum import Enum

from msgspec import Struct


class CandleWidth(int, Enum):
    integer_1 = 1
    integer_2 = 2
    integer_4 = 4
    integer_8 = 8
    integer_16 = 16
    integer_32 = 32


class HistoricalCandlesRequest(Struct):
    candle_width: CandleWidth
    end_date: str
    start_date: str
    symbol: str

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(HistoricalCandlesRequest, HistoricalCandlesResponse, "/json.architect.Marketdata/HistoricalCandles")

