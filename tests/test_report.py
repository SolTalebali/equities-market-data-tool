"""Tests for the report module."""

import pandas as pd
from src.report import summarize, write_errors, write_processed


def test_summarize():
    df = pd.DataFrame({
        'ticker': ['AAPL', 'AAPL', 'GOOGL', 'GOOGL'],
        'daily_return':[10, 20, 10, 30],
        'spread':[20, 40, 30, 40],
        'volume':[1000, 2000, 1000, 3000],
    })
    df = summarize(df)
    for col in ['mean_daily_return', 'mean_spread', 'total_volume']:
        assert col in df.columns
    assert len(df) == 2
    assert df['total_volume'].iloc[0] == 3000