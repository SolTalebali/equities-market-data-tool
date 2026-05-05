"""Tests for the transform module."""

import pandas as pd
import pytest
from src.transform import add_spread, add_daily_return, add_moving_average, add_volume_change


def test_add_spread():
    df = pd.DataFrame({
        'high': [10],
        'low': [8],
    })
    df = add_spread(df)
    assert "spread" in df.columns
    assert df["spread"].iloc[0] == 2.0


def test_add_daily_return():
    df = pd.DataFrame({
        'ticker': ['AAPL','AAPL'],
        'trade_date': ['01-03-2026', '02-03-2026'],
        'close': [100, 110],
    })
    df = add_daily_return(df)
    assert "daily_return" in df.columns
    assert df["daily_return"].iloc[1] == pytest.approx(0.10)


def test_add_volume_change():
    df = pd.DataFrame({
        'ticker': ['GOOGL', 'GOOGL'],
        'trade_date': ['01-03-2026', '02-03-2026'],
        'volume': [1000, 1500],
    })
    df = add_volume_change(df)
    assert 'volume_change' in df.columns
    assert df['volume_change'].iloc[1] == pytest.approx(0.5)


def test_add_moving_average():
    df = pd.DataFrame({
        'ticker': [ 'GOOGL', 'GOOGL', 'GOOGL'],
        'trade_date': ['01-03-2026','02-03-2026', '03-03-2026'],
        'close': [10,20,30],
    })
    df = add_moving_average(df, 3)
    assert f"moving_average_3" in df.columns
    assert df[f"moving_average_3"].iloc[2] == pytest.approx(20.0)