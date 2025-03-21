# generated by datamodel-codegen:
#   filename:  Health/HealthCheckResponse.json

from __future__ import annotations

from typing import Any, Dict, Optional

from msgspec import Struct

from .. import definitions


class HealthCheckResponse(Struct, omit_defaults=True):
    status: definitions.HealthStatus
    metrics: Optional[Dict[str, Any]] = None

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        status: definitions.HealthStatus,
        metrics: Optional[Dict[str, Any]] = None,
    ):
        return cls(
            status,
            metrics,
        )

    def __str__(self) -> str:
        return f"HealthCheckResponse(status={self.status},metrics={self.metrics})"
