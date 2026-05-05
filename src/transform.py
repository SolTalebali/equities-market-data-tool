"""Transformation module.

Applies derived calculations to validated market data, such as moving
averages, returns, and other engineered features used in the report.
"""

import pandas as pd


def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Add a column with the moving average of close prices to the DataFrame."""
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df[f"moving_average_{window}"] = df.groupby("ticker")["close"].transform(lambda x: x.rolling(window).mean())
    return df


def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """Add a daily return column to the DataFrame."""
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df['daily_return'] = df.groupby("ticker")["close"].pct_change()
    return df


def add_spread(df: pd.DataFrame) -> pd.DataFrame:
    """Add a spread column (high - low) to the DataFrame."""
    df = df.copy()
    df['spread'] = df['high'] - df['low']
    return df


def add_volume_change(df: pd.DataFrame) -> pd.DataFrame:
    """Add a daily volume change column to the DataFrame."""
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df['volume_change'] = df.groupby("ticker")["volume"].pct_change()
    return df
