# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any

from pydantic import Field

from .base_model import BaseModel


class SendTwapAlgoRequest(BaseModel):
    create_twap_algo: Any = Field(alias="createTwapAlgo")
