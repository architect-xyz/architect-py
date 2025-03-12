# generated by datamodel-codegen:
#   filename:  Orderflow/Orderflow.json

from __future__ import annotations

from typing import Annotated, Union

from msgspec import Meta

from .. import definitions
from ..Oms.Cancel import Cancel
from ..Oms.Order import Order


class OrderPending(Order, omit_defaults=True, tag_field="t", tag="w"):
    pass


class TypedOrderAck(definitions.OrderAck, omit_defaults=True, tag_field="t", tag="a"):
    pass


class TypedOrderReject(
    definitions.OrderReject, omit_defaults=True, tag_field="t", tag="r"
):
    pass


class TypedOrderOut(definitions.OrderOut, omit_defaults=True, tag_field="t", tag="o"):
    pass


class OrderReconciledOut(
    definitions.OrderOut, omit_defaults=True, tag_field="t", tag="ox"
):
    pass


class TypedOrderStale(
    definitions.OrderStale, omit_defaults=True, tag_field="t", tag="z"
):
    pass


class CancelPending(Cancel, omit_defaults=True, tag_field="t", tag="xc"):
    pass


class TypedCancelReject(
    definitions.CancelReject, omit_defaults=True, tag_field="t", tag="xr"
):
    pass


class TypedOrderCanceling(
    definitions.OrderCanceling, omit_defaults=True, tag_field="t", tag="xa"
):
    pass


class TypedOrderCanceled(
    definitions.OrderCanceled, omit_defaults=True, tag_field="t", tag="xx"
):
    pass


class TypedFill(definitions.Fill, omit_defaults=True, tag_field="t", tag="f"):
    pass


class TypedAberrantFill(
    definitions.AberrantFill, omit_defaults=True, tag_field="t", tag="af"
):
    pass


Orderflow = Annotated[
    Union[
        OrderPending,
        TypedOrderAck,
        TypedOrderReject,
        TypedOrderOut,
        OrderReconciledOut,
        TypedOrderStale,
        CancelPending,
        TypedCancelReject,
        TypedOrderCanceling,
        TypedOrderCanceled,
        TypedFill,
        TypedAberrantFill,
    ],
    Meta(title="Orderflow"),
]
