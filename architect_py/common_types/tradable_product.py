from typing import Optional

import msgspec


class TradableProduct(str):
    """
    Example instantiations:
        TradableProduct("ES 20250321 CME Future", "USD")
        TradableProduct("ES 20250321 CME Future/USD")
        (these are equivalent)

    This type exists to enforce the
    {base}/{quote} format for strings

    A base is the product that is being priced in terms of the quote.
    For example,
    "ES 20250321 CME Future/USD" means that the ES 20250321 CME Future is priced in USD.
    "ES 20250321 CME Future/EUR" means that the ES 20250321 CME Future is priced in EUR.
    "ES 20250321 CME Future/BTC" means that the ES 20250321 CME Future is priced in BTC
        (such a product does not exist on any exchange though).

    For example in a currency pair, the base is the first currency and the quote is the second currency.
    In the currency pair USD/EUR, USD is the base and EUR is the quote.
    USD/EUR = 1.1234 means that 1 USD = 1.1234 EUR
    EUR/USD = 0.8901 means that 1 EUR = 0.8901 USD
    """

    def __new__(
        cls, base_or_value: str, quote: Optional[str] = None
    ) -> "TradableProduct":
        """
        These are equivalent:
            TradableProduct("ES 20250321 CME Future", "USD")
            TradableProduct("ES 20250321 CME Future/USD")
        """
        if quote is None:
            value = base_or_value
        else:
            value = f"{base_or_value}/{quote}"

        assert "/" in value, (
            f"TradableProduct must be in the form of 'base/quote'. Got: {base_or_value}"
        )
        return super().__new__(cls, value)

    def base_quote(self) -> list[str]:
        return self.split("/")

    def base(self) -> str:
        return self.split("/", 1)[0]

    def quote(self) -> str:
        return self.split("/", 1)[1]

    def serialize(self) -> msgspec.Raw:
        return msgspec.Raw(msgspec.json.encode(str(self)))

    @staticmethod
    def deserialize(s: str) -> "TradableProduct":
        return TradableProduct(s)


def parse_tradable_product(value: str) -> TradableProduct:
    """
    For ariadne-codegen
    """
    return TradableProduct(value)
