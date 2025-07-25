# generated by datamodel-codegen:
#   filename:  OptionsMarketdata/OptionsChain.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .OptionsContract import OptionsContract


class OptionsChain(Struct, omit_defaults=True):
    calls: List[OptionsContract]
    puts: List[OptionsContract]

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        calls: List[OptionsContract],
        puts: List[OptionsContract],
    ):
        return cls(
            calls,
            puts,
        )

    def __str__(self) -> str:
        return f"OptionsChain(calls={self.calls},puts={self.puts})"
