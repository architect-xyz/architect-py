# generated by datamodel-codegen:
#   filename:  Folio/HistoricalOrdersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.HistoricalOrdersResponse import (
    HistoricalOrdersResponse,
)

from datetime import datetime
from typing import Annotated, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class HistoricalOrdersRequest(Struct, omit_defaults=True):
    account: Optional[definitions.AccountIdOrName] = None
    from_inclusive: Optional[datetime] = None
    limit: Optional[
        Annotated[Optional[int], Meta(description="Default maximum is 1000.", ge=0)]
    ] = None
    """
    Default maximum is 1000.
    """
    order_ids: Optional[
        Annotated[
            List[definitions.OrderId],
            Meta(description="if order_ids is not empty, the limit field is ignored"),
        ]
    ] = None
    """
    if order_ids is not empty, the limit field is ignored
    """
    parent_order_id: Optional[definitions.OrderId] = None
    to_exclusive: Optional[datetime] = None
    trader: Optional[definitions.TraderIdOrEmail] = None
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return HistoricalOrdersResponse

    @staticmethod
    def get_unannotated_response_type():
        return HistoricalOrdersResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Folio/HistoricalOrders"

    @staticmethod
    def get_rpc_method():
        return "unary"
