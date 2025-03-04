# generated by datamodel-codegen:
#   filename:  DropcopyRequest.json

from __future__ import annotations
import grpc
import msgspec
from architect_py.grpc_client.Orderflow.Dropcopy import Dropcopy
from architect_py.grpc_client.request import RequestStream


from typing import Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class DropcopyRequest(Struct):
    aberrant_fills: Optional[bool] = False
    account: Optional[AccountIdOrName] = None
    execution_venue: Optional[str] = None
    fills: Optional[bool] = True
    orders: Optional[bool] = False
    trader: Optional[TraderIdOrEmail] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryStreamMultiCallable["DropcopyRequest", Dropcopy]:
        return channel.unary_stream(
            "/json.architect.Orderflow/Dropcopy",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Dropcopy
            ),
        )

DropcopyRequestRequestHelper = RequestStream(DropcopyRequest, Dropcopy, "/json.architect.Orderflow/Dropcopy")
