# generated by datamodel-codegen:
#   filename:  HistoricalOrdersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.HistoricalOrdersResponse import HistoricalOrdersResponse
import grpc
import msgspec

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

AccountIdOrName = str


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


TraderIdOrEmail = str


class HistoricalOrdersRequest(Struct):
    account: Optional[AccountIdOrName] = None
    from_inclusive: Optional[str] = None
    limit: Optional[
        Annotated[Optional[int], Meta(description='Default maximum is 1000.', ge=0)]
    ] = None
    order_ids: Optional[
        Annotated[
            List[OrderId],
            Meta(description='if order_ids is not empty, the limit field is ignored'),
        ]
    ] = None
    parent_order_id: Optional[OrderId] = None
    to_exclusive: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None
    venue: Optional[str] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryUnaryMultiCallable["HistoricalOrdersRequest", HistoricalOrdersResponse]:
        return channel.unary_unary(
            "/json.architect.Folio/HistoricalOrders",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=HistoricalOrdersResponse
            ),
        )
