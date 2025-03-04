import msgspec
from typing import AsyncIterator, Callable, Generic, TypeVar, Type, ParamSpec
import grpc

from architect_py.grpc_client.Marketdata.Trade import Trade

TReq = TypeVar("TReq", bound=msgspec.Struct)
TRes = TypeVar("TRes", bound=msgspec.Struct)
P = ParamSpec("P")


class RequestStream(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes]
    route: str


class RequestUnary(msgspec.Struct, Generic[TReq, TRes, P]):
    request: Callable[P, TReq]
    response: Type[TRes]
    route: str
