# generated by datamodel-codegen:
#   filename:  Folio/HistoricalFillsResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .. import definitions


class HistoricalFillsResponse(Struct, omit_defaults=True):
    aberrant_fills: List[definitions.AberrantFill]
    fills: List[definitions.Fill]

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        aberrant_fills: List[definitions.AberrantFill],
        fills: List[definitions.Fill],
    ):
        return cls(
            aberrant_fills,
            fills,
        )

    def __str__(self) -> str:
        return f"HistoricalFillsResponse(aberrant_fills={self.aberrant_fills},fills={self.fills})"
