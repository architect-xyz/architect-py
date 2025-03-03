# generated by datamodel-codegen:
#   filename:  HealthCheckRequest.json

from __future__ import annotations
from architect_py.grpc_client.Health.HealthCheckResponse import HealthCheckResponse
import grpc
import msgspec

from typing import Annotated, Optional

from msgspec import Meta, Struct


class HealthCheckRequest(Struct):
    service: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="The service to check status for; if not provided, status of the queried server overall is returned.\n\nGenerally, this will only be set when querying the API gateway.  It's not recommended to rely on internal subservice names being stable."
            ),
        ]
    ] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryUnaryMultiCallable["HealthCheckRequest", HealthCheckResponse]:
        return channel.unary_unary(
            "/json.architect.Health/Check",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=HealthCheckResponse
            ),
        )
