import bisect
from decimal import Decimal


def update_orderbook_side(
    orderbook_side: list[list[Decimal]],
    price: Decimal,
    size: Decimal,
    ascending: bool,
) -> None:
    """
    Updates a sorted order list (either ascending for asks or descending for bids)
    using binary search to insert, update, or remove the given price level.
    """
    if ascending:
        idx = bisect.bisect_left(orderbook_side, [price, Decimal(0)])
    else:
        lo, hi = 0, len(orderbook_side)
        while lo < hi:
            mid = (lo + hi) // 2
            if orderbook_side[mid][0] > price:
                lo = mid + 1
            else:
                hi = mid
        idx = lo

    if idx < len(orderbook_side) and orderbook_side[idx][0] == price:
        if size.is_zero():
            orderbook_side.pop(idx)
        else:
            # Update the size.
            orderbook_side[idx][1] = size
    else:
        if not size.is_zero():
            orderbook_side.insert(idx, [price, size])
