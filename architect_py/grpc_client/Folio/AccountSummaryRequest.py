# generated by datamodel-codegen:
#   filename:  Folio/AccountSummaryRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountSummary import AccountSummary

from msgspec import Struct

from .. import definitions


class AccountSummaryRequest(Struct, omit_defaults=True):
    account: definitions.AccountIdOrName

    @staticmethod
    def get_response_type():
        return AccountSummary

    @staticmethod
    def get_unannotated_response_type():
        return AccountSummary

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Folio/AccountSummary"

    @staticmethod
    def get_unary_type():
        return "unary"
