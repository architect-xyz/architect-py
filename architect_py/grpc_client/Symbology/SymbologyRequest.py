# generated by datamodel-codegen:
#   filename:  Symbology/SymbologyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.SymbologySnapshot import SymbologySnapshot

from msgspec import Struct


class SymbologyRequest(Struct, omit_defaults=True):
    pass

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
    ):
        return cls()

    def __str__(self) -> str:
        return f"SymbologyRequest()"

    @staticmethod
    def get_response_type():
        return SymbologySnapshot

    @staticmethod
    def get_unannotated_response_type():
        return SymbologySnapshot

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Symbology/Symbology"

    @staticmethod
    def get_rpc_method():
        return "unary"
