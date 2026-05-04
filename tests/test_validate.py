"""Tests for the validate module."""

import pandas as pd
import pytest

from src.validate import validate_schema


def test_validate_schema_with_correct_data_types():
    df = pd.DataFrame({
        'ticker': ['AAPL', 'GOOGL'],
        'trade_date': ['2024-01-01', '2024-01-02'],
        'open': [150.0, 2800.0],
        'high': [155.0, 2850.0],
        'low': [149.0, 2750.0],
        'close': [154.0, 2820.0],
        'volume': [1000000, 1500000]
    })
    validated_df = validate_schema(df)
    assert isinstance(validated_df, pd.DataFrame)
    assert pd.api.types.is_datetime64_any_dtype(validated_df['trade_date'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        assert pd.api.types.is_numeric_dtype(validated_df[col])


def test_validate_schema_with_incorrect_data():
    df = pd.DataFrame({
        'ticker': ['AAPL'],
        'trade_date': ['2024-01-01']
    })
    with pytest.raises(ValueError):
        validate_schema(df)
       