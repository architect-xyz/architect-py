# generated by datamodel-codegen:
#   filename:  Folio/AccountHistoryRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountHistoryResponse import AccountHistoryResponse

from datetime import datetime
from typing import Optional

from msgspec import Struct

from .. import definitions


class AccountHistoryRequest(Struct, omit_defaults=True):
    account: definitions.AccountIdOrName
    from_inclusive: Optional[datetime] = None
    to_exclusive: Optional[datetime] = None

    @staticmethod
    def get_response_type():
        return AccountHistoryResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Folio/AccountHistory"

    @staticmethod
    def get_unary_type():
        return "unary"
