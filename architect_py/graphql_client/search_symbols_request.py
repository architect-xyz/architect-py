# Generated by ariadne-codegen
# Source: queries.graphql

from typing import List

from pydantic import Field

from .base_model import BaseModel


class SearchSymbolsRequest(BaseModel):
    symbology: "SearchSymbolsRequestSymbology"


class SearchSymbolsRequestSymbology(BaseModel):
    search_symbols: List[str] = Field(alias="searchSymbols")


SearchSymbolsRequest.model_rebuild()
