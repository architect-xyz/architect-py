# generated by datamodel-codegen:
#   filename:  Health/HealthCheckResponse.json

from __future__ import annotations

from msgspec import Struct

from .. import definitions


class HealthCheckResponse(Struct):
    status: definitions.HealthStatus
