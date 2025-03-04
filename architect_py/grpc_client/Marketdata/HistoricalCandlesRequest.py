# generated by datamodel-codegen:
#   filename:  HistoricalCandlesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.HistoricalCandlesResponse import HistoricalCandlesResponse
import grpc
import msgspec

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
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryUnaryMultiCallable["HistoricalCandlesRequest", HistoricalCandlesResponse]:
        return channel.unary_unary(
            "/json.architect.Marketdata/HistoricalCandles",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=HistoricalCandlesResponse
            ),
        )
