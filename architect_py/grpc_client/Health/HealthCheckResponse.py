# generated by datamodel-codegen:
#   filename:  Health/HealthCheckResponse.json

from __future__ import annotations

from msgspec import Struct

from .. import definitions


class HealthCheckResponse(Struct, omit_defaults=True):
    status: definitions.HealthStatus

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        status: definitions.HealthStatus,
    ):
        return cls(
            status,
        )

    def __str__(self) -> str:
        return f"HealthCheckResponse(status={self.status})"
