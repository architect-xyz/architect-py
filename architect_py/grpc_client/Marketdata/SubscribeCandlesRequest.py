# generated by datamodel-codegen:
#   filename:  SubscribeCandlesRequest.json

from __future__ import annotations
import grpc
import msgspec
from architect_py.grpc_client.Marketdata.Candle import Candle
from architect_py.grpc_client.request import RequestStream


from enum import Enum
from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class CandleWidth(int, Enum):
    integer_1 = 1
    integer_2 = 2
    integer_4 = 4
    integer_8 = 8
    integer_16 = 16
    integer_32 = 32


class SubscribeCandlesRequest(Struct):
    symbol: str
    candle_widths: Optional[
        Annotated[
            List[CandleWidth],
            Meta(description='If None, subscribe from all candle widths on the feed'),
        ]
    ] = None
    venue: Optional[str] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryStreamMultiCallable["SubscribeCandlesRequest", Candle]:
        return channel.unary_stream(
            "/json.architect.Marketdata/SubscribeCandles",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Candle
            ),
        )

request = RequestStream(SubscribeCandlesRequest, Candle, "/json.architect.Marketdata/SubscribeCandles")
