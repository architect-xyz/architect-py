# generated by datamodel-codegen:
#   filename:  Oms/OpenOrdersResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .. import definitions


class OpenOrdersResponse(Struct):
    open_orders: List[definitions.Order]
