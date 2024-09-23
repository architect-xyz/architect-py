import datetime
from typing import Optional

import pytz

import yfinance as yf


def fetch_prices(tickers: list[str]):
    for ticker in tickers:
        fetch_price(ticker)


def fetch_price(ticker_name: str):
    ticker = yf.Ticker(ticker_name)

    info = ticker.info

    price: Optional[str] = info.get("regularMarketPrice", None)

    exchange_timezone = info.get("exchangeTimezoneName", None)
    exchange_timezone_short = info.get("exchangeTimezoneShortName", None)

    if exchange_timezone != "N/A":
        exchange_tz = pytz.timezone(exchange_timezone)
        current_time = datetime.now(exchange_tz)
        print(
            f"Current time in {exchange_timezone_short}: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    else:
        current_time = datetime.now()
        print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"{ticker} Price: {current_price}")


# Step 3: Fetch the data
spx = yf.Ticker("^GSPC")  # SPX index ticker symbol
spy = yf.Ticker("SPY")  # SPY stock ticker symbol

# Step 4: Extract the current prices
spx_price = spx.info["regularMarketPrice"]
spy_price = spy.info["regularMarketPrice"]

print(f"SPX Index Price: {spx_price}")
print(f"SPY Stock Price: {spy_price}")
