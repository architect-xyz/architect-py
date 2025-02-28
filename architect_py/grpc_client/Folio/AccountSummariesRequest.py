# generated by datamodel-codegen:
#   filename:  AccountSummariesRequest.json

from __future__ import annotations
from architect_py.grpc_client.Folio.AccountSummariesResponse import AccountSummariesResponse
import grpc
import msgspec

from typing import Annotated, List, Optional

from msgspec import Meta, Struct

AccountIdOrName = str


TraderIdOrEmail = str


class AccountSummariesRequest(Struct):
    accounts: Optional[
        Annotated[
            List[AccountIdOrName],
            Meta(
                description='If trader and accounts are both None, return all accounts for the user'
            ),
        ]
    ] = None
    trader: Optional[TraderIdOrEmail] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryUnaryMultiCallable:
        return channel.unary_unary(
            "/json.architect.Folio/AccountSummaries",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=AccountSummariesResponse
            ),
        )
