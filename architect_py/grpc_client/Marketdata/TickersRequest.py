# generated by datamodel-codegen:
#   filename:  TickersRequest.json

from __future__ import annotations
import grpc
import msgspec
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
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryUnaryMultiCallable["TickersRequest", TickersResponse]:
        return channel.unary_unary(
            "/json.architect.Marketdata/Tickers",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=TickersResponse
            ),
        )

request = RequestUnary(TickersRequest, TickersResponse, "/json.architect.Marketdata/Tickers")
