# generated by datamodel-codegen:
#   filename:  PendingCancelsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Oms.PendingCancelsResponse import PendingCancelsResponse
import grpc
import msgspec

from typing import List, Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class PendingCancelsRequest(Struct):
    account: Optional[AccountIdOrName] = None
    cancel_ids: Optional[List[str]] = None
    symbol: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None
    venue: Optional[str] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryUnaryMultiCallable:
        return channel.unary_unary(
            "/json.architect.Oms/PendingCancels",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=PendingCancelsResponse
            ),
        )
