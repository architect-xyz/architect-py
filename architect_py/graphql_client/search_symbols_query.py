# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Annotated, List

from pydantic import BeforeValidator, Field

from architect_py.scalars import TradableProduct, parse_tradable_product

from .base_model import BaseModel


class SearchSymbolsQuery(BaseModel):
    symbology: "SearchSymbolsQuerySymbology"


class SearchSymbolsQuerySymbology(BaseModel):
    search_symbols: List[
        Annotated[TradableProduct, BeforeValidator(parse_tradable_product)]
    ] = Field(alias="searchSymbols")


SearchSymbolsQuery.model_rebuild()
