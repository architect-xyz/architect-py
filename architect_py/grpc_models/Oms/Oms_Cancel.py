# generated by datamodel-codegen:
#   filename:  Oms_Cancel.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional

from msgspec import Meta, Struct


class CancelStatus(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_127 = 127


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class Cancel(Struct):
    id: OrderId
    o: CancelStatus
    tn: Annotated[int, Meta(ge=0)]
    ts: int
    xid: str
    r: Optional[str] = None
