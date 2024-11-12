# Generated by ariadne-codegen
# Source: queries.async.graphql

from typing import List

from architect_py.scalars import AccountId

from .base_model import BaseModel


class GetAccounts(BaseModel):
    accounts: List["GetAccountsAccounts"]


class GetAccountsAccounts(BaseModel):
    id: AccountId
    name: str


GetAccounts.model_rebuild()
