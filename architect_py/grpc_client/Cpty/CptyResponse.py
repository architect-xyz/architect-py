# generated by datamodel-codegen:
#   filename:  Cpty/CptyResponse.json

from __future__ import annotations

from typing import Annotated

from msgspec import Meta

from ..Oms import Order

CptyResponse = Annotated[Order, Meta(title="CptyResponse")]
