"""
Utility functions for decoding and understanding Architect symbols.
"""

from datetime import date, datetime
from typing import Optional


def nominative_expiration(symbol: str) -> Optional[date]:
    """
    For futures and options symbols, extract the expiration date.

    Args:
        symbol: e.g. "ES 20211217 CME Future" -> date(2021, 12, 17)

    Returns:
        The expiration date as a date object
        None if the symbol is not a future or option

    To get a more precise expiration time or certain rare situations
    involving timezone skews, use get_product_info from AsyncClient
    or Client instead, which looks up actual product facts from the
    symbology service.
    """
    try:
        _, d, *_ = symbol.split(" ")
        return datetime.strptime(d, "%Y%m%d").date()
    except ValueError:
        return None
