# generated by datamodel-codegen:
#   filename:  Folio/AccountSummariesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountSummariesResponse import (
    AccountSummariesResponse,
)

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class AccountSummariesRequest(Struct, omit_defaults=True):
    accounts: Optional[
        Annotated[
            List[definitions.AccountIdOrName],
            Meta(
                description="If trader and accounts are both None, return all accounts for the user"
            ),
        ]
    ] = None
    """
    If trader and accounts are both None, return all accounts for the user
    """
    trader: Optional[definitions.TraderIdOrEmail] = None

    @staticmethod
    def get_response_type():
        return AccountSummariesResponse

    @staticmethod
    def get_unannotated_response_type():
        return AccountSummariesResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Folio/AccountSummaries"

    @staticmethod
    def get_rpc_method():
        return "unary"
