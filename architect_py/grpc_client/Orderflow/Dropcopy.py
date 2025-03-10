# generated by datamodel-codegen:
#   filename:  Orderflow/Dropcopy.json

from __future__ import annotations

from typing import Annotated, Union

from msgspec import Meta

from .. import definitions
from ..Oms.Order import Order

Dropcopy = Annotated[
    Union[Order, definitions.Fill, definitions.AberrantFill], Meta(title="Dropcopy")
]
