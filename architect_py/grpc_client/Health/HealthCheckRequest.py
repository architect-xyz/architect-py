# generated by datamodel-codegen:
#   filename:  Health/HealthCheckRequest.json

from __future__ import annotations
from architect_py.grpc_client.Health.HealthCheckResponse import HealthCheckResponse
from architect_py.grpc_client.request import RequestUnary


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
    """
    The service to check status for; if not provided, status of the queried server overall is returned.

    Generally, this will only be set when querying the API gateway.  It's not recommended to rely on internal subservice names being stable.
    """

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(HealthCheckRequest, HealthCheckResponse, "/json.architect.Health/Check")

