# generated by datamodel-codegen:
#   filename:  Symbology/SymbolsResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct


class SymbolsResponse(Struct, omit_defaults=True):
    symbols: List[str]

    # below is a constructor that takes all field titles as arguments for convenience
    @staticmethod
    def new(
        symbols: List[str],
    ) -> "SymbolsResponse":
        return SymbolsResponse(
            symbols,
        )

    def __str__(self) -> str:
        return f"SymbolsResponse(symbols={self.symbols})"
