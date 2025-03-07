# generated by datamodel-codegen:
#   filename:  Folio/AccountHistoryRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountHistoryResponse import AccountHistoryResponse

from typing import Optional

from msgspec import Struct

from .. import definitions


class AccountHistoryRequest(Struct):
    account: definitions.AccountIdOrName
    from_inclusive: Optional[str] = None
    to_exclusive: Optional[str] = None

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


ResponseType = AccountHistoryResponse
route = "/json.architect.Folio/AccountHistory"
unary_type = "unary"
