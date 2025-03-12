# generated by datamodel-codegen:
#   filename:  Orderflow/Dropcopy.json

from __future__ import annotations

from typing import Annotated, Union

from msgspec import Meta

from .. import definitions
from ..Oms.Order import Order


class TypedOrder(Order, tag="t", tag_field="o"):
    pass


class TypedFill(definitions.Fill, tag="t", tag_field="f"):
    pass


class TypedAberrantFill(definitions.AberrantFill, tag="t", tag_field="af"):
    pass


Dropcopy = Annotated[
    Union[TypedOrder, TypedFill, TypedAberrantFill], Meta(title="Dropcopy")
]
