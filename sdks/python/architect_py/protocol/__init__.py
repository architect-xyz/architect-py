"""
Wire protocol generic definitions.
"""

from dataclasses import dataclass
from typing import Any, Optional


class ProtocolException(Exception):
    pass


@dataclass(kw_only=True)
class ProtocolMessage:
    type: str

    def __post_init__(self):
        if self.type not in [
            "query",
            "response",
            "subscribe",
            "unsubscribe",
            "update",
        ]:
            raise ProtocolException(f"Invalid message type: {self.type}")


@dataclass(kw_only=True)
class ProtocolQueryMessage(ProtocolMessage):
    id: int
    method: str
    params: Optional[dict] = None


@dataclass(kw_only=True)
class ProtocolError:
    code: int
    message: str


@dataclass(kw_only=True)
class ProtocolResponseMessage(ProtocolMessage):
    id: int
    result: Optional[Any] = None
    error: Optional[ProtocolError] = None


@dataclass(kw_only=True)
class ProtocolSubscribeMessage(ProtocolMessage):
    id: int
    topic: str
