# Generated by ariadne-codegen
# Source: ../../queries.async.graphql

from typing import Any

from pydantic import Field

from .base_model import BaseModel


class SendPovAlgoRequest(BaseModel):
    create_pov_algo: Any = Field(alias="createPovAlgo")
