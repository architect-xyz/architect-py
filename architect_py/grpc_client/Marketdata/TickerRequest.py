# generated by datamodel-codegen:
#   filename:  TickerRequest.json

from __future__ import annotations
import grpc
import msgspec
from architect_py.grpc_client.Marketdata.Ticker import Ticker
from architect_py.grpc_client.request import RequestUnary


from typing import Optional

from msgspec import Struct


class TickerRequest(Struct):
    symbol: str
    venue: Optional[str] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryUnaryMultiCallable["TickerRequest", Ticker]:
        return channel.unary_unary(
            "/json.architect.Marketdata/Ticker",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Ticker
            ),
        )

TickerRequestRequestHelper = RequestUnary(TickerRequest, Ticker, "/json.architect.Marketdata/Ticker")
