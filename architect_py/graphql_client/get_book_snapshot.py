# Generated by ariadne-codegen
# Source: queries.graphql

from decimal import Decimal
from typing import Any, List

from pydantic import Field

from .base_model import BaseModel


class GetBookSnapshot(BaseModel):
    book_snapshot: "GetBookSnapshotBookSnapshot" = Field(alias="bookSnapshot")


class GetBookSnapshotBookSnapshot(BaseModel):
    timestamp: Any
    bids: List["GetBookSnapshotBookSnapshotBids"]
    asks: List["GetBookSnapshotBookSnapshotAsks"]


class GetBookSnapshotBookSnapshotBids(BaseModel):
    price: Decimal
    amount: Decimal
    total: Decimal


class GetBookSnapshotBookSnapshotAsks(BaseModel):
    price: Decimal
    amount: Decimal
    total: Decimal


GetBookSnapshot.model_rebuild()
GetBookSnapshotBookSnapshot.model_rebuild()
