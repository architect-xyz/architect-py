# generated by datamodel-codegen:
#   filename:  Symbology/SymbolsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.SymbolsResponse import SymbolsResponse

from msgspec import Struct


class SymbolsRequest(Struct):
    """
    List all symbols
    """

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


ResponseType = SymbolsResponse
route = "/json.architect.Symbology/Symbols"
unary_type = "unary"
