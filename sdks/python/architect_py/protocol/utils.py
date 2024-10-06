"""
Some utility functions to make conversions from orjson.loads to dataclasses easier.
"""

import uuid
from decimal import Decimal


def valid_decimal(v: Decimal | str) -> Decimal:
    if isinstance(v, str):
        return Decimal(v)
    elif isinstance(v, Decimal):
        return v
    else:
        raise TypeError("value must be a Decimal or a str")


def valid_uuid(v: uuid.UUID | str) -> uuid.UUID:
    if isinstance(v, str):
        return uuid.UUID(v)
    elif isinstance(v, uuid.UUID):
        return v
    else:
        raise TypeError("value must be a UUID or a str")
