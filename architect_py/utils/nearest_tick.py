from decimal import (
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_UP,
    ROUND_UP,
    Decimal,
)
from enum import Enum


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

    ROUND = ROUND_HALF_UP
    CEIL = ROUND_CEILING
    FLOOR = ROUND_FLOOR
    TOWARD_ZERO = ROUND_DOWN
    AWAY_FROM_ZERO = ROUND_UP

    def __call__(self, value: Decimal, tick_size: Decimal) -> Decimal:
        """
        Rounds the value to the nearest tick size using the specified method.

        Args:
            value: The Decimal value to be rounded.
            tick_size: The size of the tick to which the value should be rounded. Must be positive.

        Returns:
            The rounded Decimal value.
        """
        if tick_size <= Decimal(0):
            raise ValueError("tick_size must be positive")

        return value.quantize(tick_size, rounding=self.value)
