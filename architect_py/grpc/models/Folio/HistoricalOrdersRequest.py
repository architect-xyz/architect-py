# generated by datamodel-codegen:
#   filename:  Folio/HistoricalOrdersRequest.json

from __future__ import annotations
from architect_py.grpc.models.Folio.HistoricalOrdersResponse import (
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
        Annotated[Optional[int], Meta(description="Default maximum is 1000.")]
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

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        account: Optional[definitions.AccountIdOrName] = None,
        from_inclusive: Optional[datetime] = None,
        limit: Optional[int] = None,
        order_ids: Optional[List[definitions.OrderId]] = None,
        parent_order_id: Optional[definitions.OrderId] = None,
        to_exclusive: Optional[datetime] = None,
        trader: Optional[definitions.TraderIdOrEmail] = None,
        venue: Optional[str] = None,
    ):
        return cls(
            account,
            from_inclusive,
            limit,
            order_ids,
            parent_order_id,
            to_exclusive,
            trader,
            venue,
        )

    def __str__(self) -> str:
        return f"HistoricalOrdersRequest(account={self.account},from_inclusive={self.from_inclusive},limit={self.limit},order_ids={self.order_ids},parent_order_id={self.parent_order_id},to_exclusive={self.to_exclusive},trader={self.trader},venue={self.venue})"

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
