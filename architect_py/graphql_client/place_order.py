# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import OrderFields


class PlaceOrder(BaseModel):
    oms: "PlaceOrderOms"


class PlaceOrderOms(BaseModel):
    place_order: "PlaceOrderOmsPlaceOrder" = Field(alias="placeOrder")


class PlaceOrderOmsPlaceOrder(OrderFields):
    pass


PlaceOrder.model_rebuild()
PlaceOrderOms.model_rebuild()
