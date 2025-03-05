from decimal import Decimal

from architect_py.utils.nearest_tick import TickRoundMethod


def test_rounding():
    # Example usage
    value = Decimal("123.454")
    tick_size = Decimal("0.01")

    rounded_value = TickRoundMethod.ROUND(value, tick_size=tick_size)
    assert rounded_value == Decimal("123.45")

    rounded_ceil = TickRoundMethod.CEIL(value, tick_size)
    assert rounded_ceil == Decimal("123.46")

    rounded_floor = TickRoundMethod.FLOOR(value, tick_size)
    assert rounded_floor == Decimal("123.45")

    rounded_floor = TickRoundMethod.FLOOR(Decimal("123.459"), tick_size)
    assert rounded_floor == Decimal("123.45")

    rounded_toward_zero_pos = TickRoundMethod.TOWARD_ZERO(value, tick_size)
    assert rounded_toward_zero_pos == Decimal("123.45")

    value_negative = Decimal("-123.456")
    rounded_toward_zero_neg = TickRoundMethod.TOWARD_ZERO(value_negative, tick_size)
    assert rounded_toward_zero_neg == Decimal("-123.45")

    rounded_away_from_zero_pos = TickRoundMethod.AWAY_FROM_ZERO(value, tick_size)
    assert rounded_away_from_zero_pos == Decimal("123.46")

    rounded_away_from_zero_neg = TickRoundMethod.AWAY_FROM_ZERO(
        value_negative, tick_size
    )
    assert rounded_away_from_zero_neg == Decimal("-123.46")


if __name__ == "__main__":
    test_rounding()
    print("rounding.py: All tests passed!")
