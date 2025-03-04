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


TReq = TypeVar("TReq", bound=msgspec.Struct)
TRes = TypeVar("TRes", bound=msgspec.Struct)
P = ParamSpec("P")


class RequestStream(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str


class RequestUnary(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str
