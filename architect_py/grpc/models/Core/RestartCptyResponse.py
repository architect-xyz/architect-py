# generated by datamodel-codegen:
#   filename:  Core/RestartCptyResponse.json

from __future__ import annotations

from msgspec import Struct


class RestartCptyResponse(Struct, omit_defaults=True):
    pass

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
    ):
        return cls()

    def __str__(self) -> str:
        return f"RestartCptyResponse()"
