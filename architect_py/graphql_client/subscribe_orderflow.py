# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Optional, Union
from uuid import UUID

from pydantic import BeforeValidator, Field

from architect_py.scalars import OrderDir, graphql_parse_order_dir

from .base_model import BaseModel
from .enums import FillKind
from .fragments import OrderFields


class SubscribeOrderflow(BaseModel):
    orderflow: Union[
        "SubscribeOrderflowOrderflowOrder",
        "SubscribeOrderflowOrderflowOrderAck",
        "SubscribeOrderflowOrderflowGqlOrderReject",
        "SubscribeOrderflowOrderflowOrderOut",
        "SubscribeOrderflowOrderflowOrderStale",
        "SubscribeOrderflowOrderflowCancel",
        "SubscribeOrderflowOrderflowCancelReject",
        "SubscribeOrderflowOrderflowOrderCanceling",
        "SubscribeOrderflowOrderflowOrderCanceled",
        "SubscribeOrderflowOrderflowFill",
        "SubscribeOrderflowOrderflowAberrantFill",
    ] = Field(discriminator="typename__")


class SubscribeOrderflowOrderflowOrder(OrderFields):
    typename__: Literal["Order"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowOrderAck(BaseModel):
    typename__: Literal["OrderAck"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")


class SubscribeOrderflowOrderflowGqlOrderReject(BaseModel):
    typename__: Literal["GqlOrderReject"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")
    reason: str
    message: Optional[str]


class SubscribeOrderflowOrderflowOrderOut(BaseModel):
    typename__: Literal["OrderOut"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")


class SubscribeOrderflowOrderflowOrderStale(BaseModel):
    typename__: Literal["OrderStale"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")


class SubscribeOrderflowOrderflowCancel(BaseModel):
    typename__: Literal["Cancel"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowCancelReject(BaseModel):
    typename__: Literal["CancelReject"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")
    message: Optional[str]


class SubscribeOrderflowOrderflowOrderCanceling(BaseModel):
    typename__: Literal["OrderCanceling"] = Field(alias="__typename")


class SubscribeOrderflowOrderflowOrderCanceled(BaseModel):
    typename__: Literal["OrderCanceled"] = Field(alias="__typename")
    order_id: str = Field(alias="orderId")
    cancel_id: Optional[UUID] = Field(alias="cancelId")


class SubscribeOrderflowOrderflowFill(BaseModel):
    typename__: Literal["Fill"] = Field(alias="__typename")
    fill_order_id: Optional[str] = Field(alias="fillOrderId")
    fill_id: UUID = Field(alias="fillId")
    fill_kind: FillKind = Field(alias="fillKind")
    execution_venue: str = Field(alias="executionVenue")
    exchange_fill_id: Optional[str] = Field(alias="exchangeFillId")
    symbol: str
    dir: Annotated[OrderDir, BeforeValidator(graphql_parse_order_dir)]
    quantity: Decimal
    price: Decimal
    recv_time: Optional[datetime] = Field(alias="recvTime")
    trade_time: Optional[datetime] = Field(alias="tradeTime")


class SubscribeOrderflowOrderflowAberrantFill(BaseModel):
    typename__: Literal["AberrantFill"] = Field(alias="__typename")


SubscribeOrderflow.model_rebuild()
