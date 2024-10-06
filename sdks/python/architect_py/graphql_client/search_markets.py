# Generated by ariadne-codegen
# Source: ../../queries.graphql

from typing import List

from pydantic import Field

from .base_model import BaseModel
from .fragments import MarketFields


class SearchMarkets(BaseModel):
    filter_markets: List["SearchMarketsFilterMarkets"] = Field(alias="filterMarkets")


class SearchMarketsFilterMarkets(MarketFields):
    pass


SearchMarkets.model_rebuild()
