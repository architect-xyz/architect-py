# generated by datamodel-codegen:
#   filename:  Accounts/AccountsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Accounts.AccountsResponse import AccountsResponse
from architect_py.grpc_client.request import RequestUnary


from typing import Annotated, Optional

from msgspec import Meta, Struct

TraderIdOrEmail = str


class AccountsRequest(Struct):
    trader: Optional[
        Annotated[
            Optional[TraderIdOrEmail],
            Meta(
                description='Request accounts from the perspective of this trader; if not specified, defaults to the caller user.'
            ),
        ]
    ] = None
    """
    Request accounts from the perspective of this trader; if not specified, defaults to the caller user.
    """

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(AccountsRequest, AccountsResponse, "/json.architect.Accounts/Accounts")

