from types import UnionType
from typing import Any, Protocol, Type, TypeVar

import msgspec

from architect_py.common_types import TradableProduct


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, TradableProduct):
        return str(obj)


encoder = msgspec.json.Encoder(enc_hook=enc_hook)
decoders: dict[type | UnionType, msgspec.json.Decoder] = {}


ResponseTypeGeneric = TypeVar("ResponseTypeGeneric", covariant=True)


class RequestType(Protocol[ResponseTypeGeneric]):
    @staticmethod
    def get_unannotated_response_type() -> Type[ResponseTypeGeneric]: ...

    @staticmethod
    def get_response_type() -> Type[ResponseTypeGeneric]: ...

    @staticmethod
    def get_route() -> str: ...

    @staticmethod
    def get_rpc_method() -> Any: ...
