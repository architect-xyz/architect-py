# Generated by ariadne-codegen
# Source: queries.async.graphql

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
    price: Any
    amount: Any
    total: Any


class GetBookSnapshotBookSnapshotAsks(BaseModel):
    price: Any
    amount: Any
    total: Any


GetBookSnapshot.model_rebuild()
GetBookSnapshotBookSnapshot.model_rebuild()
