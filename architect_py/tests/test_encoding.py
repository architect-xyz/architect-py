from datetime import datetime, timezone

from architect_py.common_types.time_in_force import TimeInForce
from architect_py.common_types.tradable_product import TradableProduct
from architect_py.grpc.utils import encoder


def test_encoding():
    product = TradableProduct("ES 20250321 CME Future", "USD")
    encoded = encoder.encode(product)

    assert encoded == b'"ES 20250321 CME Future/USD"', (
        'Encoding of TradableProduct failed, expected "ES 20250321 CME Future/USD" but got '
        + str(encoded)
    )

    now = datetime.now(timezone.utc)

    encoded = encoder.encode(TimeInForce.GTD(now))

    assert encoded == b'{"GTD": "' + now.isoformat().encode() + b'"}', (
        'Encoding of TimeInForce.GTD failed, expected {"GTD": "'
        + now.isoformat()
        + '"} but got '
        + str(encoded)
    )

    encoded = encoder.encode(TimeInForce.GTC)

    assert encoded == b'"GTC"', (
        'Encoding of TimeInForce.GTC failed, expected "GTC" but got ' + str(encoded)
    )


if __name__ == "__main__":
    test_encoding()
    print("All tests passed.")
