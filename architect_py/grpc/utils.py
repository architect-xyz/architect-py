from types import UnionType
from typing import Any, Protocol, Type, TypeVar

import msgspec


def enc_hook(obj: Any) -> Any:
    return obj.serialize()


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
