# Generated by ariadne-codegen
# Source: queries.async.graphql

from typing import Any, List

from pydantic import Field

from .base_model import BaseModel


class CancelOrders(BaseModel):
    cancel_orders: List[Any] = Field(alias="cancelOrders")
