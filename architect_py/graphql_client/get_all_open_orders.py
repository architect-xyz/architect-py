# Generated by ariadne-codegen
# Source: queries.graphql

from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import OrderFields


class GetAllOpenOrders(BaseModel):
    oms: "GetAllOpenOrdersOms"


class GetAllOpenOrdersOms(BaseModel):
    open_orders: List["GetAllOpenOrdersOmsOpenOrders"] = Field(alias="openOrders")


class GetAllOpenOrdersOmsOpenOrders(OrderFields):
    pass


GetAllOpenOrders.model_rebuild()
GetAllOpenOrdersOms.model_rebuild()
