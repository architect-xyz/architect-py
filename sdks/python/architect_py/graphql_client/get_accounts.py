# Generated by ariadne-codegen
# Source: ../../queries.graphql

from typing import Any, List

from .base_model import BaseModel


class GetAccounts(BaseModel):
    accounts: List["GetAccountsAccounts"]


class GetAccountsAccounts(BaseModel):
    id: Any
    name: str


GetAccounts.model_rebuild()
