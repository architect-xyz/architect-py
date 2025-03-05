import msgspec
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    Type,
    ParamSpec,
    Annotated,
)


# TReq = TypeVar("TReq", bound=msgspec.Struct)
TReq = TypeVar("TReq")
TRes = TypeVar("TRes")  # cannot be bound to msgspec.Struct because of Union types
P = ParamSpec("P")


class RequestStream(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str


class RequestUnary(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str


class Tag(msgspec.Struct):
    t: str
