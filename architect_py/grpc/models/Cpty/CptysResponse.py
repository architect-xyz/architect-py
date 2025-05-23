# generated by datamodel-codegen:
#   filename:  Cpty/CptysResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .CptyStatus import CptyStatus


class CptysResponse(Struct, omit_defaults=True):
    cptys: List[CptyStatus]

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        cptys: List[CptyStatus],
    ):
        return cls(
            cptys,
        )

    def __str__(self) -> str:
        return f"CptysResponse(cptys={self.cptys})"
