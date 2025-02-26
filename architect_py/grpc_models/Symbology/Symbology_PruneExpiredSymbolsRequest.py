# generated by datamodel-codegen:
#   filename:  Symbology_PruneExpiredSymbolsRequest.json

from __future__ import annotations

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
