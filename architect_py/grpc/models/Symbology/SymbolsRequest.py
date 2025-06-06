# generated by datamodel-codegen:
#   filename:  Symbology/SymbolsRequest.json

from __future__ import annotations
from architect_py.grpc.models.Symbology.SymbolsResponse import SymbolsResponse

from msgspec import Struct


class SymbolsRequest(Struct, omit_defaults=True):
    """
    List all symbols
    """

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
    ):
        return cls()

    def __str__(self) -> str:
        return f"SymbolsRequest()"

    @staticmethod
    def get_response_type():
        return SymbolsResponse

    @staticmethod
    def get_unannotated_response_type():
        return SymbolsResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Symbology/Symbols"

    @staticmethod
    def get_rpc_method():
        return "unary"
