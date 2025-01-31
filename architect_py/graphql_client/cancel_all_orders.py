# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel


class CancelAllOrders(BaseModel):
    oms: "CancelAllOrdersOms"


class CancelAllOrdersOms(BaseModel):
    cancel_all_orders: bool = Field(alias="cancelAllOrders")


CancelAllOrders.model_rebuild()
