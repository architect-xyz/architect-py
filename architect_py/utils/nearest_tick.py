"""
Example Usage:

tick_size = get_tick_size(market_id, client)
nearest_tick(123.456, TickRoundMethod.ROUND, tick_size)
"""

from enum import Enum

from functools import partial

import sys

"""
This conditional import is to deal with
FutureWarning: functools.partial will be a method descriptor in future Python versions; wrap it in enum.member() if you want to preserve the old behavior
given on Python 3.12+
"""
if sys.version_info >= (3, 11):
    from .nearest_tick_2 import *
else:

    from decimal import (
        Decimal,
        ROUND_CEILING,
        ROUND_DOWN,
        ROUND_FLOOR,
        ROUND_HALF_UP,
        ROUND_UP,
    )

    def round_method(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        ROUND: Round to the nearest tick. If the remainder is >= half the tick size, round up; otherwise, round down.
        """
        assert tick_size > 0, "Tick size should be positive"
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
        assert tick_size > 0, "Tick size should be positive"
        remainder = value % tick_size
        return (value - remainder + tick_size).quantize(
            tick_size, rounding=ROUND_CEILING
        )

    def floor_method(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        FLOOR: Always round down to the nearest tick.
        """
        assert tick_size > 0, "Tick size should be positive"
        remainder = value % tick_size
        return (value - remainder).quantize(tick_size, rounding=ROUND_FLOOR)

    def toward_zero_method(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        TOWARD_ZERO: Round towards zero.
        """
        assert tick_size > 0, "Tick size should be positive"
        remainder = value % tick_size
        if value >= 0:
            return (value - remainder).quantize(tick_size, rounding=ROUND_DOWN)
        else:
            return (value - remainder).quantize(tick_size, rounding=ROUND_UP)

    def away_from_zero_method(value: Decimal, tick_size: Decimal) -> Decimal:
        """
        AWAY_FROM_ZERO: Round away from zero.
        """
        assert tick_size > 0, "Tick size should be positive"
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
        treated as method definitions instead of attributes, which messes up their usage

        This was fixed in Python 3.11, where the @member and @nonmember decorators were added to solve this issue
        however, as we want to be compatible with Python 3.10, we will use the partial function from the functools module


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
            tick_round_method.value(123.456, tick_size)
            # would return Decimal("123.46")

            tick_round_method = TickRoundMethod.FLOOR
            tick_round_method.value(123.456, tick_size)
            # would return Decimal("123.45")

        """

        ROUND = partial(round_method)
        CEIL = partial(ceil_method)
        FLOOR = partial(floor_method)
        TOWARD_ZERO = partial(toward_zero_method)
        AWAY_FROM_ZERO = partial(away_from_zero_method)

        def __call__(self, *args, **kwargs):
            return self.value(*args, **kwargs)
