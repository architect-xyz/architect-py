# generated by datamodel-codegen:
#   filename:  Folio/AccountHistoryRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountHistoryResponse import AccountHistoryResponse
from architect_py.grpc_client.request import RequestUnary


from typing import Optional

from msgspec import Struct

from .. import definitions


class AccountHistoryRequest(Struct):
    account: definitions.AccountIdOrName
    from_inclusive: Optional[str] = None
    to_exclusive: Optional[str] = None

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(AccountHistoryRequest, AccountHistoryResponse, "/json.architect.Folio/AccountHistory")

