# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BeforeValidator, Field

from architect_py.scalars import OrderDir, graphql_parse_order_dir

from .base_model import BaseModel
from .enums import FillKind


class GetFillsQuery(BaseModel):
    folio: "GetFillsQueryFolio"


class GetFillsQueryFolio(BaseModel):
    historical_fills: "GetFillsQueryFolioHistoricalFills" = Field(
        alias="historicalFills"
    )


class GetFillsQueryFolioHistoricalFills(BaseModel):
    fills: List["GetFillsQueryFolioHistoricalFillsFills"]
    aberrant_fills: List["GetFillsQueryFolioHistoricalFillsAberrantFills"] = Field(
        alias="aberrantFills"
    )


class GetFillsQueryFolioHistoricalFillsFills(BaseModel):
    fill_id: UUID = Field(alias="fillId")
    fill_kind: FillKind = Field(alias="fillKind")
    execution_venue: str = Field(alias="executionVenue")
    exchange_fill_id: Optional[str] = Field(alias="exchangeFillId")
    order_id: Optional[str] = Field(alias="orderId")
    trader: Optional[str]
    account: Optional[UUID]
    symbol: str
    dir: Annotated[OrderDir, BeforeValidator(graphql_parse_order_dir)]
    quantity: Decimal
    price: Decimal
    recv_time: Optional[datetime] = Field(alias="recvTime")
    trade_time: Optional[datetime] = Field(alias="tradeTime")


class GetFillsQueryFolioHistoricalFillsAberrantFills(BaseModel):
    fill_id: UUID = Field(alias="fillId")
    fill_kind: Optional[FillKind] = Field(alias="fillKind")
    execution_venue: str = Field(alias="executionVenue")
    exchange_fill_id: Optional[str] = Field(alias="exchangeFillId")
    order_id: Optional[str] = Field(alias="orderId")
    trader: Optional[str]
    account: Optional[UUID]
    symbol: Optional[str]
    dir: Optional[Annotated[OrderDir, BeforeValidator(graphql_parse_order_dir)]]
    quantity: Optional[Decimal]
    price: Optional[Decimal]
    recv_time: Optional[datetime] = Field(alias="recvTime")
    trade_time: Optional[datetime] = Field(alias="tradeTime")


GetFillsQuery.model_rebuild()
GetFillsQueryFolio.model_rebuild()
GetFillsQueryFolioHistoricalFills.model_rebuild()
