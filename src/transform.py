"""Transformation module.

Applies derived calculations to validated market data, such as moving
averages, returns, and other engineered features used in the report.
"""

import pandas as pd


def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Add a moving average column to the DataFrame."""
    pass


def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """Add a daily return column to the DataFrame."""
    pass
