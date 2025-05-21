from typing import TYPE_CHECKING, List

import msgspec
import pandas as pd

if TYPE_CHECKING:
    from .. import Candle

CANDLES_FIELD_MAP = {
    "av": "sell_volume",
    "bv": "buy_volume",
    "s": "symbol",
    "v": "volume",
    "w": "width",
    "ac": "ask_close",
    "ah": "ask_high",
    "al": "ask_low",
    "ao": "ask_open",
    "bc": "bid_close",
    "bh": "bid_high",
    "bl": "bid_low",
    "bo": "bid_open",
    "c": "close",
    "h": "high",
    "l": "low",
    "mc": "mid_close",
    "mh": "mid_high",
    "ml": "mid_low",
    "mo": "mid_open",
    "o": "open",
}


def candles_to_dataframe(candles: List["Candle"]) -> pd.DataFrame:
    records = msgspec.to_builtins(candles)
    df = pd.DataFrame.from_records(records)
    df.rename(columns=CANDLES_FIELD_MAP, inplace=True)
    df["timestamp"] = pd.to_datetime(
        df["ts"] * 1_000_000_000 + df["tn"],
        unit="ns",
        utc=True,
    )
    df.style.hide(["tn", "ts"], axis=1)
    df.set_index("timestamp", inplace=True)
    return df
