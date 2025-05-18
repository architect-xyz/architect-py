from datetime import datetime
from typing import ClassVar, Literal, Optional

import msgspec


class TimeInForce:
    """
    A type-checker-friendly way to get enum-like constants + a payload-carrying variant (GTD) in one class.
    Usage:
    Simply use the class as an enum for the standard time in force values:
        TimeInForce.GTC  # Good Till Cancelled
        TimeInForce.DAY  # Day Order
        TimeInForce.IOC  # Immediate or Cancel
        TimeInForce.FOK  # Fill or Kill
        TimeInForce.ATO  # At the Opening
        TimeInForce.ATC  # At the Close

    To specify a GTD (Good Till Date) order, use the GTD method:
        TimeInForce.GTD(datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
        TimeInForce.GTD(datetime.now(timezone.utc))
    """

    __slots__ = ("kind", "date")
    kind: Literal["GTC", "DAY", "IOC", "FOK", "ATO", "ATC", "GTD"]
    date: Optional[datetime]

    GTC: ClassVar["TimeInForce"]
    DAY: ClassVar["TimeInForce"]
    IOC: ClassVar["TimeInForce"]
    FOK: ClassVar["TimeInForce"]
    ATO: ClassVar["TimeInForce"]
    ATC: ClassVar["TimeInForce"]

    def __init__(
        self,
        kind: Literal["GTC", "DAY", "IOC", "FOK", "ATO", "ATC", "GTD"],
        date: Optional[datetime] = None,
    ) -> None:
        self.kind = kind
        self.date = date

    @classmethod
    def GTD(cls, when: datetime) -> "TimeInForce":
        return cls("GTD", when)

    def serialize(self) -> msgspec.Raw:
        if self.kind == "GTD":
            assert self.date is not None
            return msgspec.Raw(f'{{"GTD": "{self.date.isoformat()}"}}'.encode())
        return msgspec.Raw('"{self.kind}"'.encode())

    @staticmethod
    def deserialize(s) -> "TimeInForce":
        if isinstance(s, dict):
            return TimeInForce.GTD(datetime.fromisoformat(s["GTD"]))
        return TimeInForce(s)

    def __repr__(self) -> str:
        if self.kind == "GTD":
            assert self.date is not None
            return f"<TimeInForce.GTD({self.date.isoformat()})>"
        return f"<TimeInForce.{self.kind}>"


TimeInForce.GTC = TimeInForce("GTC")
TimeInForce.DAY = TimeInForce("DAY")
TimeInForce.IOC = TimeInForce("IOC")
TimeInForce.FOK = TimeInForce("FOK")
TimeInForce.ATO = TimeInForce("ATO")
TimeInForce.ATC = TimeInForce("ATC")
