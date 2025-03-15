"""
For when python version is 3.11 or higher.

Example Usage:

tick_size = get_tick_size(market_id, client)
nearest_tick(123.456, TickRoundMethod.ROUND, tick_size)
"""

from decimal import (
    Decimal,
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_UP,
    ROUND_UP,
)

from enum import Enum, member


class TickRoundMethod(Enum):
    """
    ENUM VALUES:
        ROUND
        CEIL
        FLOOR
        TOWARD_ZERO
        AWAY_FROM_ZERO

    Enum that stores functions for rounding a given value to the nearest tick size based on the specified rounding method.

    Function Parameters:
    - value (Decimal): The value to be rounded.
    - tick_size (Decimal): The size of the tick to which the value should be rounded. Should be positive

    Returns:
    - Decimal: The value rounded to the nearest tick size.

    Example Usage:
        tick_size = get_tick_size(market_id, client)
        # assume tick_size is Decimal("0.01")

        tick_round_method = TickRoundMethod.ROUND
        tick_round_method(123.456, tick_size)
        # would return Decimal("123.46")

        tick_round_method = TickRoundMethod.FLOOR
        tick_round_method(123.456, tick_size)
        # would return Decimal("123.45")
    """

    @member
    @staticmethod
    def ROUND(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        ROUND: Round to the nearest tick. If the remainder is >= half the tick size, round up; otherwise, round down.
        """
        remainder = value % tick_size
        if remainder >= tick_size / 2:
            return (value - remainder + tick_size).quantize(
                tick_size, rounding=ROUND_HALF_UP
            )
        else:
            return (value - remainder).quantize(tick_size, rounding=ROUND_HALF_UP)

    @member
    @staticmethod
    def CEIL(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        CEIL: Always round up to the nearest tick.
        """
        remainder = value % tick_size
        return (value - remainder + tick_size).quantize(
            tick_size, rounding=ROUND_CEILING
        )

    @member
    @staticmethod
    def FLOOR(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        FLOOR: Always round down to the nearest tick.
        """
        remainder = value % tick_size
        return (value - remainder).quantize(tick_size, rounding=ROUND_FLOOR)

    @member
    @staticmethod
    def TOWARD_ZERO(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        TOWARD_ZERO: Round towards zero.
        """
        remainder = value % tick_size
        if value >= 0:
            return (value - remainder).quantize(tick_size, rounding=ROUND_DOWN)
        else:
            return (value - remainder).quantize(tick_size, rounding=ROUND_UP)

    @member
    @staticmethod
    def AWAY_FROM_ZERO(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        AWAY_FROM_ZERO: Round away from zero.
        """
        remainder = value % tick_size
        if value >= 0:
            if remainder != 0:
                return (value - remainder + tick_size).quantize(
                    tick_size, rounding=ROUND_UP
                )
            else:
                return value.quantize(tick_size, rounding=ROUND_UP)
        else:
            if remainder != 0:
                return (value - remainder - tick_size).quantize(
                    tick_size, rounding=ROUND_DOWN
                )
            else:
                return value.quantize(tick_size, rounding=ROUND_DOWN)

    def __call__(self, value: Decimal, tick_size: Decimal) -> Decimal:
        return self.value(value, tick_size)
