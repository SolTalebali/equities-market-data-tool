"""Generate a synthetic market_prices.csv for development and testing.

Produces 60 trading days of OHLCV data for 8 tickers using a random walk,
then deliberately injects ~30 bad rows (missing values, negative prices,
high<low, malformed dates, negative volume, missing ticker) so the
validation stage has something to reject. Output: data/raw/market_prices.csv.

Run from the project root:
    python scripts/generate_sample_data.py
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
TICKERS = ["AAPL", "MSFT", "GOOGL", "BARC", "HSBC", "BP", "LLOY", "VOD"]
N_DAYS = 60
START_DATE = "2024-01-02"

START_PRICES = {
    "AAPL": 185.0,
    "MSFT": 375.0,
    "GOOGL": 140.0,
    "BARC": 1.55,
    "HSBC": 6.30,
    "BP": 4.70,
    "LLOY": 0.48,
    "VOD": 0.70,
}

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "market_prices.csv"


def trading_days(start: str, n: int) -> pd.DatetimeIndex:
    """Return n consecutive weekdays starting from `start` (skipping Sat/Sun)."""
    return pd.bdate_range(start=start, periods=n)


def build_clean_frame() -> pd.DataFrame:
    """Build a clean OHLCV frame using a per-ticker random walk."""
    rng = np.random.default_rng(SEED)
    dates = trading_days(START_DATE, N_DAYS)
    rows = []
    for ticker in TICKERS:
        price = START_PRICES[ticker]
        for d in dates:
            step = rng.normal(loc=0.0, scale=0.015) * price
            open_ = max(price + rng.normal(0, 0.005) * price, 0.01)
            close = max(price + step, 0.01)
            high = max(open_, close) + abs(rng.normal(0, 0.004)) * price
            low = min(open_, close) - abs(rng.normal(0, 0.004)) * price
            low = max(low, 0.01)
            volume = int(rng.integers(5_000_000, 100_000_000))
            rows.append(
                {
                    "ticker": ticker,
                    "trade_date": d.strftime("%Y-%m-%d"),
                    "open": round(open_, 4),
                    "high": round(high, 4),
                    "low": round(low, 4),
                    "close": round(close, 4),
                    "volume": volume,
                }
            )
            price = close
    return pd.DataFrame(rows)


def inject_bad_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Mutate ~30 rows in-place across six different failure modes."""
    rng = random.Random(SEED)
    df = df.copy()
    n = len(df)

    def pick(k: int) -> list[int]:
        return rng.sample(range(n), k)

    # Missing close price
    for i in pick(5):
        df.at[i, "close"] = np.nan

    # Negative price (vary which OHLC column)
    for i in pick(5):
        col = rng.choice(["open", "high", "low", "close"])
        df.at[i, col] = -abs(df.at[i, col]) if pd.notna(df.at[i, col]) else -1.23

    # high < low (swap them)
    for i in pick(5):
        h, l = df.at[i, "high"], df.at[i, "low"]
        df.at[i, "high"], df.at[i, "low"] = l, h

    # Invalid date format
    bad_date_formats = ["01/02/2024", "Jan 2 2024", "2024.03.15", "15-03-2024", "not-a-date"]
    for i in pick(5):
        df.at[i, "trade_date"] = rng.choice(bad_date_formats)

    # Negative volume
    for i in pick(5):
        df.at[i, "volume"] = -abs(int(df.at[i, "volume"]))

    # Missing ticker
    for i in pick(5):
        df.at[i, "ticker"] = np.nan

    return df


def main() -> None:
    clean = build_clean_frame()
    dirty = inject_bad_rows(clean)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dirty.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(dirty)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
