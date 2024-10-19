"""
Example Usage:

tick_size = get_tick_size(market_id, client)
nearest_tick(123.456, TickRoundMethod.ROUND, tick_size)
"""

from decimal import (
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_UP,
    ROUND_UP,
    Decimal,
)


from enum import Enum

from functools import partial, lru_cache

from architect_py.async_client import AsyncClient
from architect_py.client import Client


@lru_cache(maxsize=10, typed=False)
def get_tick_size(market_id: str, client: Client) -> Decimal:
    market = client.get_market(market_id)
    if market is None:
        raise ValueError(f"Market {market_id} not found")
    return Decimal(market.tick_size)


@lru_cache(maxsize=10, typed=False)
async def get_tick_size_async(market_id: str, client: AsyncClient) -> Decimal:
    market = await client.get_market(market_id)
    if market is None:
        raise ValueError(f"Market {market_id} not found")
    return Decimal(market.tick_size)


# Define the rounding functions
def round_method(value: Decimal, tick_size: Decimal) -> Decimal:
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


def ceil_method(value: Decimal, tick_size: Decimal) -> Decimal:
    """
    CEIL: Always round up to the nearest tick.
    """
    remainder = value % tick_size
    return (value - remainder + tick_size).quantize(tick_size, rounding=ROUND_CEILING)


def floor_method(value: Decimal, tick_size: Decimal) -> Decimal:
    """
    FLOOR: Always round down to the nearest tick.
    """
    remainder = value % tick_size
    return (value - remainder).quantize(tick_size, rounding=ROUND_FLOOR)


def toward_zero_method(value: Decimal, tick_size: Decimal) -> Decimal:
    """
    TOWARD_ZERO: Round towards zero.
    """
    remainder = value % tick_size
    if value >= 0:
        return (value - remainder).quantize(tick_size, rounding=ROUND_DOWN)
    else:
        return (value - remainder).quantize(tick_size, rounding=ROUND_UP)


def away_from_zero_method(value: Decimal, tick_size: Decimal) -> Decimal:
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


class TickRoundMethod(Enum):
    """
    We would want to map the enum values to functions, however, the
    issue with functions is that Python does not treat them normally and are
    tretaed as method definitions instead of attributes, which messes up their usage

    This was fixed in Python 3.11, where the @member and @nonmember decorators were added to solve this issue
    however, as we want to be compatible with Python 3.10, we will use the partial function from the functools module
    """

    ROUND = partial(round_method)
    CEIL = partial(ceil_method)
    FLOOR = partial(floor_method)
    TOWARD_ZERO = partial(toward_zero_method)
    AWAY_FROM_ZERO = partial(away_from_zero_method)

    def apply(self, value: Decimal, tick_size: Decimal) -> Decimal:
        """
        Apply the rounding method to the given value based on tick size.

        Parameters:
        - value (Decimal): The value to be rounded.
        - tick_size (Decimal): The size of the tick to which the value should be rounded.

        Returns:
        - Decimal: The value rounded to the nearest tick size.
        """
        return self.value(value, tick_size)


def nearest_tick(
    value: Decimal, method: TickRoundMethod, tick_size: Decimal
) -> Decimal:
    """
    Rounds the given value to the nearest tick size based on the specified rounding method.

    Parameters:
    - value (Decimal): The value to be rounded.
    - method (RoundMethod): The rounding method to apply.
    - tick_size (Decimal): The size of the tick to which the value should be rounded.

    Returns:
    - Decimal: The value rounded to the nearest tick size.

    Raises:
    - ValueError: If an unknown rounding method is provided or if tick_size is non-positive.

    Example:
        tick_size = get_tick_size(market_id, client)
        nearest_tick(123.456, TickRoundMethod.ROUND, tick_size)
    """
    if tick_size <= 0:
        raise ValueError("tick_size must be positive.")
    return method.apply(value, tick_size)


if __name__ == "__main__":
    from decimal import Decimal

    # Example usage
    value = Decimal("123.454")
    tick_size = Decimal("0.01")

    print(f"Value: {value}, Tick Size: {tick_size}")

    rounded_value = nearest_tick(
        value, method=TickRoundMethod.ROUND, tick_size=tick_size
    )
    print(f"Rounded Value: {rounded_value}")  # Output: Rounded Value: 123.46

    # Additional examples
    rounded_ceil = nearest_tick(value, TickRoundMethod.CEIL, tick_size)
    print(f"CEIL: {rounded_ceil}")  # Output: CEIL: 123.46

    rounded_floor = nearest_tick(value, TickRoundMethod.FLOOR, tick_size)
    print(f"FLOOR: {rounded_floor}")  # Output: FLOOR: 123.45

    rounded_toward_zero_pos = nearest_tick(
        value, TickRoundMethod.TOWARD_ZERO, tick_size
    )
    print(
        f"TOWARD_ZERO (Positive): {rounded_toward_zero_pos}"
    )  # Output: TOWARD_ZERO (Positive): 123.45

    value_negative = Decimal("-123.456")
    rounded_toward_zero_neg = nearest_tick(
        value_negative, TickRoundMethod.TOWARD_ZERO, tick_size
    )
    print(
        f"TOWARD_ZERO (Negative): {rounded_toward_zero_neg}"
    )  # Output: TOWARD_ZERO (Negative): -123.45

    rounded_away_from_zero_pos = nearest_tick(
        value, TickRoundMethod.AWAY_FROM_ZERO, tick_size
    )
    print(
        f"AWAY_FROM_ZERO (Positive): {rounded_away_from_zero_pos}"
    )  # Output: AWAY_FROM_ZERO (Positive): 123.46

    rounded_away_from_zero_neg = nearest_tick(
        value_negative, TickRoundMethod.AWAY_FROM_ZERO, tick_size
    )
    print(
        f"AWAY_FROM_ZERO (Negative): {rounded_away_from_zero_neg}"
    )  # Output: AWAY_FROM_ZERO (Negative): -123.46
