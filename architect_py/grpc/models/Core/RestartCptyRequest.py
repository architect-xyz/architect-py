# generated by datamodel-codegen:
#   filename:  Core/RestartCptyRequest.json

from __future__ import annotations
from architect_py.grpc.models.Core.RestartCptyResponse import RestartCptyResponse

from msgspec import Struct


class RestartCptyRequest(Struct, omit_defaults=True):
    cpty: str

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        cpty: str,
    ):
        return cls(
            cpty,
        )

    def __str__(self) -> str:
        return f"RestartCptyRequest(cpty={self.cpty})"

    @staticmethod
    def get_response_type():
        return RestartCptyResponse

    @staticmethod
    def get_unannotated_response_type():
        return RestartCptyResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Core/RestartCpty"

    @staticmethod
    def get_rpc_method():
        return "unary"
