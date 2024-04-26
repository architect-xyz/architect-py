# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import FillKind


class FillsSubscription(BaseModel):
    fills: "FillsSubscriptionFills"


class FillsSubscriptionFills(BaseModel):
    dir: Any
    fill_id: Any = Field(alias="fillId")
    kind: FillKind
    market_id: Any = Field(alias="marketId")
    order_id: Optional[Any] = Field(alias="orderId")
    price: Any
    quantity: Any
    recv_time: Optional[Any] = Field(alias="recvTime")
    trade_time: Any = Field(alias="tradeTime")
    market: "FillsSubscriptionFillsMarket"


class FillsSubscriptionFillsMarket(BaseModel):
    tick_size: Any = Field(alias="tickSize")
    step_size: Any = Field(alias="stepSize")
    name: str
    exchange_symbol: str = Field(alias="exchangeSymbol")


FillsSubscription.model_rebuild()
FillsSubscriptionFills.model_rebuild()