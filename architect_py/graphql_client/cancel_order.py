# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel


class CancelOrder(BaseModel):
    cancel_order: str = Field(alias="cancelOrder")
