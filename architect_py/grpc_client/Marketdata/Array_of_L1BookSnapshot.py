# generated by datamodel-codegen:
#   filename:  Marketdata/Array_of_L1BookSnapshot.json

from __future__ import annotations

from typing import Annotated, List

from msgspec import Meta

from .. import definitions

ArrayOfL1BookSnapshot = Annotated[
    List[definitions.L1BookSnapshot], Meta(title='Array_of_L1BookSnapshot')
]
