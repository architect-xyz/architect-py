# generated by datamodel-codegen:
#   filename:  Orderflow/OrderflowRequest.json

from __future__ import annotations
from architect_py.grpc_client.Orderflow.Orderflow import Orderflow

from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct

from .. import definitions


class OrderflowRequest1(Struct, tag_field="t", tag="p"):
    d: Annotated[definitions.Dir, Meta(title="dir")]
    q: Annotated[definitions.DecimalModel, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    t: Literal["p"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    k: Literal["LIMIT"]
    p: Annotated[definitions.DecimalModel, Meta(title="limit_price")]
    po: Annotated[bool, Meta(title="post_only")]
    a: Optional[
        Annotated[Optional[definitions.AccountIdOrName], Meta(title="account")]
    ] = None
    id: Optional[
        Annotated[
            Optional[definitions.OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    src: Optional[
        Annotated[Optional[definitions.OrderSource], Meta(title="source")]
    ] = None
    u: Optional[
        Annotated[Optional[definitions.TraderIdOrEmail], Meta(title="trader")]
    ] = None
    x: Optional[Annotated[Optional[str], Meta(title="execution_venue")]] = None

    @property
    def dir(self) -> definitions.Dir:
        return self.d

    @dir.setter
    def dir(self, value: definitions.Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> definitions.DecimalModel:
        return self.q

    @quantity.setter
    def quantity(self, value: definitions.DecimalModel) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> definitions.DecimalModel:
        return self.p

    @limit_price.setter
    def limit_price(self, value: definitions.DecimalModel) -> None:
        self.p = value

    @property
    def post_only(self) -> bool:
        return self.po

    @post_only.setter
    def post_only(self, value: bool) -> None:
        self.po = value

    @property
    def account(self) -> Optional[definitions.AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[definitions.AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[definitions.OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[definitions.OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[definitions.TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[definitions.TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


class OrderflowRequest2(Struct, tag_field="t", tag="p"):
    d: Annotated[definitions.Dir, Meta(title="dir")]
    q: Annotated[definitions.DecimalModel, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    t: Literal["p"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    k: Literal["STOP_LOSS_LIMIT"]
    p: Annotated[definitions.DecimalModel, Meta(title="limit_price")]
    tp: Annotated[definitions.DecimalModel, Meta(title="trigger_price")]
    a: Optional[
        Annotated[Optional[definitions.AccountIdOrName], Meta(title="account")]
    ] = None
    id: Optional[
        Annotated[
            Optional[definitions.OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    src: Optional[
        Annotated[Optional[definitions.OrderSource], Meta(title="source")]
    ] = None
    u: Optional[
        Annotated[Optional[definitions.TraderIdOrEmail], Meta(title="trader")]
    ] = None
    x: Optional[Annotated[Optional[str], Meta(title="execution_venue")]] = None

    @property
    def dir(self) -> definitions.Dir:
        return self.d

    @dir.setter
    def dir(self, value: definitions.Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> definitions.DecimalModel:
        return self.q

    @quantity.setter
    def quantity(self, value: definitions.DecimalModel) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> definitions.DecimalModel:
        return self.p

    @limit_price.setter
    def limit_price(self, value: definitions.DecimalModel) -> None:
        self.p = value

    @property
    def trigger_price(self) -> definitions.DecimalModel:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: definitions.DecimalModel) -> None:
        self.tp = value

    @property
    def account(self) -> Optional[definitions.AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[definitions.AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[definitions.OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[definitions.OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[definitions.TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[definitions.TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


class OrderflowRequest3(Struct, tag_field="t", tag="p"):
    d: Annotated[definitions.Dir, Meta(title="dir")]
    q: Annotated[definitions.DecimalModel, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    t: Literal["p"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    k: Literal["TAKE_PROFIT_LIMIT"]
    p: Annotated[definitions.DecimalModel, Meta(title="limit_price")]
    tp: Annotated[definitions.DecimalModel, Meta(title="trigger_price")]
    a: Optional[
        Annotated[Optional[definitions.AccountIdOrName], Meta(title="account")]
    ] = None
    id: Optional[
        Annotated[
            Optional[definitions.OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    src: Optional[
        Annotated[Optional[definitions.OrderSource], Meta(title="source")]
    ] = None
    u: Optional[
        Annotated[Optional[definitions.TraderIdOrEmail], Meta(title="trader")]
    ] = None
    x: Optional[Annotated[Optional[str], Meta(title="execution_venue")]] = None

    @property
    def dir(self) -> definitions.Dir:
        return self.d

    @dir.setter
    def dir(self, value: definitions.Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> definitions.DecimalModel:
        return self.q

    @quantity.setter
    def quantity(self, value: definitions.DecimalModel) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> definitions.DecimalModel:
        return self.p

    @limit_price.setter
    def limit_price(self, value: definitions.DecimalModel) -> None:
        self.p = value

    @property
    def trigger_price(self) -> definitions.DecimalModel:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: definitions.DecimalModel) -> None:
        self.tp = value

    @property
    def account(self) -> Optional[definitions.AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[definitions.AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[definitions.OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[definitions.OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[definitions.TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[definitions.TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


class OrderflowRequest4(Struct, tag_field="t", tag="x"):
    id: Annotated[definitions.OrderId, Meta(title="order_id")]
    t: Literal["x"]
    xid: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.",
                title="cancel_id",
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """

    @property
    def order_id(self) -> definitions.OrderId:
        return self.id

    @order_id.setter
    def order_id(self, value: definitions.OrderId) -> None:
        self.id = value

    @property
    def cancel_id(self) -> Optional[str]:
        return self.xid

    @cancel_id.setter
    def cancel_id(self, value: Optional[str]) -> None:
        self.xid = value

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


class OrderflowRequest5(Struct, tag_field="t", tag="xo"):
    id: str
    t: Literal["xo"]
    account: Optional[definitions.AccountIdOrName] = None
    execution_venue: Optional[str] = None
    trader: Optional[definitions.TraderIdOrEmail] = None

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


OrderflowRequest = Annotated[
    Union[
        OrderflowRequest1,
        OrderflowRequest2,
        OrderflowRequest3,
        OrderflowRequest4,
        OrderflowRequest5,
    ],
    Meta(title="OrderflowRequest"),
]


ResponseType = Orderflow
route = "/json.architect.Orderflow/Orderflow"
unary_type = "duplex_stream"
