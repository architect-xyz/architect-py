# generated by datamodel-codegen:
#   filename:  Accounts_AccountsResponse.json
#   timestamp: 2025-02-25T21:20:57+00:00

from __future__ import annotations

from typing import List

from msgspec import Struct


class AccountPermissions(Struct):
    list: bool
    reduce_or_close: bool
    set_limits: bool
    trade: bool
    view: bool


class Account(Struct):
    id: str
    name: str


class AccountWithPermissions(Struct):
    account: Account
    permissions: AccountPermissions
    trader: str


class AccountsResponse(Struct):
    accounts: List[AccountWithPermissions]
