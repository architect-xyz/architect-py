# generated by datamodel-codegen:
#   filename:  Symbology/SymbolsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.SymbolsResponse import SymbolsResponse

from msgspec import Struct


class SymbolsRequest(Struct, omit_defaults=True):
    """
    List all symbols
    """

    @staticmethod
    def get_response_type():
        return SymbolsResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Symbology/Symbols"

    @staticmethod
    def get_unary_type():
        return "unary"
