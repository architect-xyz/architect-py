# generated by datamodel-codegen:
#   filename:  Folio/HistoricalFillsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.HistoricalFillsResponse import (
    HistoricalFillsResponse,
)

from datetime import datetime
from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class HistoricalFillsRequest(Struct, omit_defaults=True):
    account: Optional[definitions.AccountIdOrName] = None
    from_inclusive: Optional[datetime] = None
    limit: Optional[
        Annotated[Optional[int], Meta(description="Default maximum is 1000.", ge=0)]
    ] = None
    """
    Default maximum is 1000.
    """
    order_id: Optional[definitions.OrderId] = None
    to_exclusive: Optional[datetime] = None
    trader: Optional[definitions.TraderIdOrEmail] = None
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return HistoricalFillsResponse

    @staticmethod
    def get_unannotated_response_type():
        return HistoricalFillsResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Folio/HistoricalFills"

    @staticmethod
    def get_unary_type():
        return "unary"
