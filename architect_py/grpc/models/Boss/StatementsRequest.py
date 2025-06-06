# generated by datamodel-codegen:
#   filename:  Boss/StatementsRequest.json

from __future__ import annotations
from architect_py.grpc.models.Boss.StatementsResponse import StatementsResponse

from msgspec import Struct


class StatementsRequest(Struct, omit_defaults=True):
    account_id: str

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        account_id: str,
    ):
        return cls(
            account_id,
        )

    def __str__(self) -> str:
        return f"StatementsRequest(account_id={self.account_id})"

    @staticmethod
    def get_response_type():
        return StatementsResponse

    @staticmethod
    def get_unannotated_response_type():
        return StatementsResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Boss/Statements"

    @staticmethod
    def get_rpc_method():
        return "unary"
