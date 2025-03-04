# generated by datamodel-codegen:
#   filename:  SubscribeTradesRequest.json

from __future__ import annotations
import grpc
import msgspec
from architect_py.grpc_client.Marketdata.Trade import Trade
from architect_py.grpc_client.request import RequestStream


from typing import Annotated, Optional

from msgspec import Meta, Struct


class SubscribeTradesRequest(Struct):
    symbol: Optional[
        Annotated[
            Optional[str],
            Meta(description='If None, subscribe from all symbols on the feed'),
        ]
    ] = None
    venue: Optional[str] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryStreamMultiCallable["SubscribeTradesRequest", Trade]:
        return channel.unary_stream(
            "/json.architect.Marketdata/SubscribeTrades",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Trade
            ),
        )

SubscribeTradesRequestRequestHelper = RequestStream(SubscribeTradesRequest, Trade, "/json.architect.Marketdata/SubscribeTrades")
