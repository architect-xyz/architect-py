# Generated by ariadne-codegen
# Source: queries.async.graphql

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from architect_py.scalars import Dir

from .base_model import BaseModel
from .enums import FillKind
from .fragments import MarketFields


class GetFills(BaseModel):
    fills: "GetFillsFills"


class GetFillsFills(BaseModel):
    normal: List["GetFillsFillsNormal"]


class GetFillsFillsNormal(BaseModel):
    kind: FillKind
    fill_id: str = Field(alias="fillId")
    order_id: Optional[str] = Field(alias="orderId")
    market: "GetFillsFillsNormalMarket"
    dir: Dir
    price: Decimal
    quantity: Decimal
    recv_time: Optional[datetime] = Field(alias="recvTime")
    trade_time: datetime = Field(alias="tradeTime")


class GetFillsFillsNormalMarket(MarketFields):
    pass


GetFills.model_rebuild()
GetFillsFills.model_rebuild()
GetFillsFillsNormal.model_rebuild()
