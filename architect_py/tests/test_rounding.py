from decimal import Decimal

from architect_py.utils.nearest_tick import TickRoundMethod, nearest_tick


def test_rounding():
    # Example usage
    value = Decimal("123.454")
    tick_size = Decimal("0.01")

    print(f"Value: {value}, Tick Size: {tick_size}")

    rounded_value = nearest_tick(
        value, method=TickRoundMethod.ROUND, tick_size=tick_size
    )
    assert rounded_value == Decimal("123.45")

    rounded_ceil = nearest_tick(value, TickRoundMethod.CEIL, tick_size)
    assert rounded_ceil == Decimal("123.46")

    rounded_floor = nearest_tick(value, TickRoundMethod.FLOOR, tick_size)
    assert rounded_floor == Decimal("123.45")

    rounded_floor = nearest_tick(Decimal("123.459"), TickRoundMethod.FLOOR, tick_size)
    assert rounded_floor == Decimal("123.45")

    rounded_toward_zero_pos = nearest_tick(
        value, TickRoundMethod.TOWARD_ZERO, tick_size
    )
    assert rounded_toward_zero_pos == Decimal("123.45")

    value_negative = Decimal("-123.456")
    rounded_toward_zero_neg = nearest_tick(
        value_negative, TickRoundMethod.TOWARD_ZERO, tick_size
    )
    assert rounded_toward_zero_neg == Decimal("-123.45")

    rounded_away_from_zero_pos = nearest_tick(
        value, TickRoundMethod.AWAY_FROM_ZERO, tick_size
    )
    assert rounded_away_from_zero_pos == Decimal("123.46")

    rounded_away_from_zero_neg = nearest_tick(
        value_negative, TickRoundMethod.AWAY_FROM_ZERO, tick_size
    )
    assert rounded_away_from_zero_neg == Decimal("-123.46")
