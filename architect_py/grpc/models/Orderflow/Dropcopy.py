# generated by datamodel-codegen:
#   filename:  Orderflow/Dropcopy.json

from __future__ import annotations

from typing import Annotated, Union

from msgspec import Meta

from .. import definitions
from ..Oms.Order import Order


class TaggedOrder(Order, omit_defaults=True, tag_field="t", tag="o"):
    pass


class TaggedFill(definitions.Fill, omit_defaults=True, tag_field="t", tag="f"):
    pass


class TaggedAberrantFill(
    definitions.AberrantFill, omit_defaults=True, tag_field="t", tag="af"
):
    pass


Dropcopy = Annotated[
    Union[TaggedOrder, TaggedFill, TaggedAberrantFill], Meta(title="Dropcopy")
]
