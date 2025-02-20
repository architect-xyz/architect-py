# Generated by ariadne-codegen
# Source: queries.graphql

from typing import List

from .base_model import BaseModel
from .fragments import AccountWithPermissionsFields


class ListAccountsQuery(BaseModel):
    user: "ListAccountsQueryUser"


class ListAccountsQueryUser(BaseModel):
    accounts: List["ListAccountsQueryUserAccounts"]


class ListAccountsQueryUserAccounts(AccountWithPermissionsFields):
    pass


ListAccountsQuery.model_rebuild()
ListAccountsQueryUser.model_rebuild()
