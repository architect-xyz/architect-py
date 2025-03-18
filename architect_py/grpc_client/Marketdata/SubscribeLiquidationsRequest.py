# generated by datamodel-codegen:
#   filename:  Marketdata/SubscribeLiquidationsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.Liquidation import Liquidation

from typing import List, Optional

from msgspec import Struct


class SubscribeLiquidationsRequest(Struct, omit_defaults=True):
    symbols: Optional[List[str]] = None

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        symbols: Optional[List[str]] = None,
    ):
        return cls(
            symbols,
        )

    def __str__(self) -> str:
        return f"SubscribeLiquidationsRequest(symbols={self.symbols})"

    @staticmethod
    def get_response_type():
        return Liquidation

    @staticmethod
    def get_unannotated_response_type():
        return Liquidation

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Marketdata/SubscribeLiquidations"

    @staticmethod
    def get_rpc_method():
        return "stream"
