# generated by datamodel-codegen:
#   filename:  Folio/AccountSummariesRequest.json

from __future__ import annotations

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class AccountSummariesRequest(Struct):
    accounts: Optional[
        Annotated[
            List[definitions.AccountIdOrName],
            Meta(
                description='If trader and accounts are both None, return all accounts for the user'
            ),
        ]
    ] = None
    """
    If trader and accounts are both None, return all accounts for the user
    """
    trader: Optional[definitions.TraderIdOrEmail] = None

    @staticmethod
    def get_response_type():
        return "&RESPONSE_TYPE:AccountSummariesRequest"

    @staticmethod
    def get_route() -> str:
        return "&ROUTE:AccountSummariesRequest"

    @staticmethod
    def get_unary_type():
        return "&UNARY_TYPE:AccountSummariesRequest"
