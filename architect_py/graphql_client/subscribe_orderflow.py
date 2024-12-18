# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import List, Literal, Optional, Union

from pydantic import Field

from architect_py.scalars import OrderDir

from .base_model import BaseModel
from .enums import FillKind, OrderSource, OrderStateFlags


class SubscribeOrderflow(BaseModel):
    orderflow: Union[
        "SubscribeOrderflowOrderflowOrder",
        "SubscribeOrderflowOrderflowOmsOrderUpdate",
        "SubscribeOrderflowOrderflowCancel",
        "SubscribeOrderflowOrderflowCancelAll",
        "SubscribeOrderflowOrderflowAck",
        "SubscribeOrderflowOrderflowReject",
        "SubscribeOrderflowOrderflowFill",
        "SubscribeOrderflowOrderflowAberrantFill",
        "SubscribeOrderflowOrderflowOut",
    ] = Field(discriminator="typename__")


class SubscribeOrderflowOrderflowOrder(BaseModel):
    typename__: Literal["Order"] = Field(alias="__typename")
    id: str
    market_id: str = Field(alias="marketId")
    dir: OrderDir
    quantity: Decimal
    account_id: Optional[str] = Field(alias="accountId")
    order_type: Union[
        "SubscribeOrderflowOrderflowOrderOrderTypeLimitOrderType",
        "SubscribeOrderflowOrderflowOrderOrderTypeStopLossLimitOrderType",
        "SubscribeOrderflowOrderflowOrderOrderTypeTakeProfitLimitOrderType",
    ] = Field(alias="orderType", discriminator="typename__")
    time_in_force: "SubscribeOrderflowOrderflowOrderTimeInForce" = Field(
        alias="timeInForce"
    )
    quote_id: Optional[str] = Field(alias="quoteId")
    source: OrderSource


class SubscribeOrderflowOrderflowOrderOrderTypeLimitOrderType(BaseModel):
    typename__: Literal["LimitOrderType"] = Field(alias="__typename")
    limit_price: Decimal = Field(alias="limitPrice")
    post_only: bool = Field(alias="postOnly")


class SubscribeOrderflowOrderflowOrderOrderTypeStopLossLimitOrderType(BaseModel):
    typename__: Literal["StopLossLimitOrderType"] = Field(alias="__typename")
    limit_price: Decimal = Field(alias="limitPrice")
    trigger_price: Decimal = Field(alias="triggerPrice")


class SubscribeOrderflowOrderflowOrderOrderTypeTakeProfitLimitOrderType(BaseModel):
    typename__: Literal["TakeProfitLimitOrderType"] = Field(alias="__typename")
    limit_price: Decimal = Field(alias="limitPrice")
    trigger_price: Decimal = Field(alias="triggerPrice")


class SubscribeOrderflowOrderflowOrderTimeInForce(BaseModel):
    instruction: str
    good_til_date: Optional[datetime] = Field(alias="goodTilDate")


class SubscribeOrderflowOrderflowOmsOrderUpdate(BaseModel):
    typename__: Literal["OmsOrderUpdate"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")
    order_state: List[OrderStateFlags] = Field(alias="orderState")
    filled_qty: Decimal = Field(alias="filledQty")
    avg_fill_price: Optional[Decimal] = Field(alias="avgFillPrice")


class SubscribeOrderflowOrderflowCancel(BaseModel):
    typename__: Literal["Cancel"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowCancelAll(BaseModel):
    typename__: Literal["CancelAll"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowAck(BaseModel):
    typename__: Literal["Ack"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")


class SubscribeOrderflowOrderflowReject(BaseModel):
    typename__: Literal["Reject"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")
    reason: str


class SubscribeOrderflowOrderflowFill(BaseModel):
    typename__: Literal["Fill"] = Field(alias="__typename")
    fill_order_id: Optional[str] = Field(alias="fillOrderId")
    fill_kind: FillKind = Field(alias="fillKind")
    market_id: str = Field(alias="marketId")
    dir: OrderDir
    price: Decimal
    quantity: Decimal
    trade_time: datetime = Field(alias="tradeTime")


class SubscribeOrderflowOrderflowAberrantFill(BaseModel):
    typename__: Literal["AberrantFill"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowOut(BaseModel):
    typename__: Literal["Out"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")


SubscribeOrderflow.model_rebuild()
SubscribeOrderflowOrderflowOrder.model_rebuild()
