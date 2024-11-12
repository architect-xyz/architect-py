# Generated by ariadne-codegen
# Source: queries.async.graphql

from decimal import Decimal
from typing import Any, Optional

from architect_py.scalars import Dir

from .base_model import BaseModel


class SubscribeTrades(BaseModel):
    trades: "SubscribeTradesTrades"


class SubscribeTradesTrades(BaseModel):
    time: Optional[Any]
    price: Decimal
    size: Decimal
    direction: Optional[Dir]


SubscribeTrades.model_rebuild()
