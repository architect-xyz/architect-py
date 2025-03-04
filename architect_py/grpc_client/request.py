import msgspec
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    Type,
    ParamSpec,
    Annotated,
    get_origin,
    get_args,
)


TReq = TypeVar("TReq", bound=msgspec.Struct)
TRes = TypeVar("TRes")
P = ParamSpec("P")


def unwrap_annotated(type_hint: Type | Annotated[Any, Any]) -> Type:
    """Extract the real type from Annotated[T, Meta(...)]"""
    if get_origin(type_hint) is Annotated:
        return get_args(type_hint)[
            0
        ]  # Extract the actual type (e.g., Union[Snapshot, Diff])
    return type_hint


class RequestStream(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str


class RequestUnary(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes] | Annotated[TRes, Any]
    route: str
