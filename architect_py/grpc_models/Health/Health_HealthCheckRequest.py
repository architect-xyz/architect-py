# generated by datamodel-codegen:
#   filename:  Health_HealthCheckRequest.json

from __future__ import annotations

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
