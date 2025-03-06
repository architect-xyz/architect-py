# generated by datamodel-codegen:
#   filename:  Symbology/PruneExpiredSymbolsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.PruneExpiredSymbolsResponse import PruneExpiredSymbolsResponse

from typing import Annotated, Optional

from msgspec import Meta, Struct


class PruneExpiredSymbolsRequest(Struct):
    cutoff: Optional[
        Annotated[
            Optional[int],
            Meta(
                description='If None then it will just use server current time; otherwise, specify a unix timestamp in seconds'
            ),
        ]
    ] = None
    """
    If None then it will just use server current time; otherwise, specify a unix timestamp in seconds
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


ResponseType = PruneExpiredSymbolsResponse
route = "/json.architect.Symbology/PruneExpiredSymbols"
unary_type = "unary"

