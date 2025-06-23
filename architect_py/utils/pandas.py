from typing import TYPE_CHECKING, List

import msgspec
import pandas as pd

if TYPE_CHECKING:
    from .. import Candle, Ticker

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


def tickers_to_dataframe(tickers: List["Ticker"]) -> pd.DataFrame:
    records = msgspec.to_builtins(tickers)
    df = pd.DataFrame.from_records(records)
    df.rename(
        columns={
            "s": "symbol",
            "ve": "venue",
            "ap": "ask_price",
            "as": "ask_size",
            "bp": "bid_price",
            "bs": "bid_size",
            "dividend": "dividend",
            "dividend_yield": "dividend_yield",
            "eps_adj": "eps_adj",
            "fr": "funding_rate",
            "ft": "next_funding_time",
            "h": "high_24h",
            "ip": "index_price",
            "isp": "indicative_settlement_price",
            "l": "low_24h",
            "market_cap": "market_cap",
            "mp": "mark_price",
            "o": "open_24h",
            "oi": "open_interest",
            "p": "last_price",
            "price_to_earnings": "price_to_earnings",
            "q": "last_size",
            "sd": "last_settlement_date",
            "shares_outstanding_weighted_adj": "shares_outstanding_weighted_adj",
            "sp": "last_settlement_price",
            "v": "volume_24h",
            "vm": "volume_30d",
            "xh": "session_high",
            "xl": "session_low",
            "xo": "session_open",
            "xv": "session_volume",
        },
        inplace=True,
    )
    df["timestamp"] = pd.to_datetime(
        df["ts"] * 1_000_000_000 + df["tn"],
        unit="ns",
        utc=True,
    )
    df.style.hide(["tn", "ts"], axis=1)
    df.set_index("symbol", inplace=True)
    return df
