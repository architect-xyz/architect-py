# generated by datamodel-codegen:
#   filename:  Folio_HistoricalFillsRequest.json

from __future__ import annotations

from typing import Annotated, Optional

from msgspec import Meta, Struct

AccountIdOrName = str


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


TraderIdOrEmail = str


class HistoricalFillsRequest(Struct):
    account: Optional[AccountIdOrName] = None
    from_inclusive: Optional[str] = None
    limit: Optional[
        Annotated[Optional[int], Meta(description='Default maximum is 1000.', ge=0)]
    ] = None
    order_id: Optional[OrderId] = None
    to_exclusive: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None
    venue: Optional[str] = None
