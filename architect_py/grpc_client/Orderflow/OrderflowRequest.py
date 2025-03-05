# generated by datamodel-codegen:
#   filename:  OrderflowRequest.json

from __future__ import annotations
from architect_py.grpc_client.Orderflow.Orderflow import Orderflow
from architect_py.grpc_client.request import RequestUnary

from decimal import Decimal


from enum import Enum
from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct

AccountIdOrName = str




class Dir(str, Enum):
    """
    An order side/direction or a trade execution side/direction. In GraphQL these are serialized as "buy" or "sell".
    """

    BUY = 'BUY'
    SELL = 'SELL'


class OrderId(Struct):
    """
    System-unique, persistent order identifiers
    """

    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class OrderSource(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3
    integer_4 = 4
    integer_5 = 5
    integer_255 = 255


class TimeInForce1(str, Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'


class TimeInForce2(Struct):
    GTD: str


TimeInForce = Union[TimeInForce1, TimeInForce2, Literal['DAY']]


TraderIdOrEmail = str


class OrderflowRequest1(Struct):
    d: Annotated[Dir, Meta(title='dir')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    t: Literal['p']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    k: Literal['LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    po: Annotated[bool, Meta(title='post_only')]
    a: Optional[Annotated[Optional[AccountIdOrName], Meta(title='account')]] = None
    id: Optional[
        Annotated[
            Optional[OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    src: Optional[Annotated[Optional[OrderSource], Meta(title='source')]] = None
    u: Optional[Annotated[Optional[TraderIdOrEmail], Meta(title='trader')]] = None
    x: Optional[Annotated[Optional[str], Meta(title='execution_venue')]] = None

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def post_only(self) -> bool:
        return self.po

    @post_only.setter
    def post_only(self, value: bool) -> None:
        self.po = value

    @property
    def account(self) -> Optional[AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_request_helper():
        return request_helper


class OrderflowRequest2(Struct):
    d: Annotated[Dir, Meta(title='dir')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    t: Literal['p']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    k: Literal['STOP_LOSS_LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    a: Optional[Annotated[Optional[AccountIdOrName], Meta(title='account')]] = None
    id: Optional[
        Annotated[
            Optional[OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    src: Optional[Annotated[Optional[OrderSource], Meta(title='source')]] = None
    u: Optional[Annotated[Optional[TraderIdOrEmail], Meta(title='trader')]] = None
    x: Optional[Annotated[Optional[str], Meta(title='execution_venue')]] = None

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def trigger_price(self) -> Decimal:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: Decimal) -> None:
        self.tp = value

    @property
    def account(self) -> Optional[AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_request_helper():
        return request_helper


class OrderflowRequest3(Struct):
    d: Annotated[Dir, Meta(title='dir')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    t: Literal['p']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    k: Literal['TAKE_PROFIT_LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    a: Optional[Annotated[Optional[AccountIdOrName], Meta(title='account')]] = None
    id: Optional[
        Annotated[
            Optional[OrderId],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through."
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    src: Optional[Annotated[Optional[OrderSource], Meta(title='source')]] = None
    u: Optional[Annotated[Optional[TraderIdOrEmail], Meta(title='trader')]] = None
    x: Optional[Annotated[Optional[str], Meta(title='execution_venue')]] = None

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def trigger_price(self) -> Decimal:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: Decimal) -> None:
        self.tp = value

    @property
    def account(self) -> Optional[AccountIdOrName]:
        return self.a

    @account.setter
    def account(self, value: Optional[AccountIdOrName]) -> None:
        self.a = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def source(self) -> Optional[OrderSource]:
        return self.src

    @source.setter
    def source(self, value: Optional[OrderSource]) -> None:
        self.src = value

    @property
    def trader(self) -> Optional[TraderIdOrEmail]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[TraderIdOrEmail]) -> None:
        self.u = value

    @property
    def execution_venue(self) -> Optional[str]:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: Optional[str]) -> None:
        self.x = value

    @staticmethod
    def get_request_helper():
        return request_helper


class OrderflowRequest4(Struct):
    id: Annotated[OrderId, Meta(title='order_id')]
    t: Literal['x']
    xid: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.",
                title='cancel_id',
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """

    @property
    def order_id(self) -> OrderId:
        return self.id

    @order_id.setter
    def order_id(self, value: OrderId) -> None:
        self.id = value

    @property
    def cancel_id(self) -> Optional[str]:
        return self.xid

    @cancel_id.setter
    def cancel_id(self, value: Optional[str]) -> None:
        self.xid = value

    @staticmethod
    def get_request_helper():
        return request_helper


class OrderflowRequest5(Struct):
    id: str
    t: Literal['xo']
    account: Optional[AccountIdOrName] = None
    execution_venue: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None

    @staticmethod
    def get_request_helper():
        return request_helper


OrderflowRequest = Annotated[
    Union[
        Union[OrderflowRequest1, OrderflowRequest2, OrderflowRequest3],
        OrderflowRequest4,
        OrderflowRequest5,
    ],
    Meta(title='OrderflowRequest'),
]


request_helper = RequestDuplex_Stream(OrderflowRequest, typing.Union[Orderflow.Orderflow1, Orderflow.Orderflow2, Orderflow.Orderflow3, Orderflow.Orderflow4, Orderflow.Orderflow5, Orderflow.Orderflow6, Orderflow.Orderflow7, Orderflow.Orderflow8, Orderflow.Orderflow9, Orderflow.Orderflow10, Orderflow.Orderflow11, Orderflow.Orderflow12, Orderflow.Orderflow13], "/json.architect.Orderflow/Orderflow")

