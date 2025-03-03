# generated by datamodel-codegen:
#   filename:  SubscribeOrderflowRequest.json

from __future__ import annotations
from architect_py.grpc_client.Orderflow.Orderflow import Orderflow
import grpc
import msgspec

from typing import Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class SubscribeOrderflowRequest(Struct):
    account: Optional[AccountIdOrName] = None
    execution_venue: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryStreamMultiCallable["SubscribeOrderflowRequest", Orderflow]:
        return channel.unary_stream(
            "/json.architect.Orderflow/SubscribeOrderflow",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Orderflow
            ),
        )
