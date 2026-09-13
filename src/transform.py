import pandas as pd
import logging

logger = logging.getLogger(__name__)


def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df[f"moving_average_{window}"] = df.groupby("ticker")["close"].transform(lambda x: x.rolling(window).mean())
    
    logger.info("Added moving_average column")
    return df


def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df['daily_return'] = df.groupby("ticker")["close"].pct_change()

    logger.info("Added daily_return column")
    return df


def add_spread(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['spread'] = df['high'] - df['low']

    logger.info("Added spread column")
    return df


def add_volume_change(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["ticker", "trade_date"])
    df['volume_change'] = df.groupby("ticker")["volume"].pct_change()
    
    logger.info("Added volume_change column")
    return df
