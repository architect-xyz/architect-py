# generated by datamodel-codegen:
#   filename:  CancelOrderRequest.json

from __future__ import annotations
from architect_py.grpc_client.Oms.Cancel import Cancel
import grpc
import msgspec

from typing import Annotated, Optional

from msgspec import Meta, Struct


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class CancelOrderRequest(Struct):
    id: Annotated[OrderId, Meta(title='order_id')]
    xid: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.",
                title='cancel_id',
            ),
        ]
    ] = None

    @property
    def order_id(self) -> OrderId:
        return self.id

    @order_id.setter
    def order_id(self, value: OrderId) -> None:
        self.id = value

    @property
    def cancel_id(self) -> Optional[str]:
        return self.xid

    @cancel_id.setter
    def cancel_id(self, value: Optional[str]) -> None:
        self.xid = value

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryUnaryMultiCallable:
        return channel.unary_unary(
            "/json.architect.Oms/CancelOrder",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=Cancel
            ),
        )
