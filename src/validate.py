"""Validation module.

Provides functions to check ingested market data for schema correctness,
type validity, and business-rule violations (e.g. high >= low, non-negative
prices and volume).
"""

import pandas as pd

EXPECTED_COLUMNS = ['ticker', 'trade_date', 'open', 'high', 'low', 'close', 'volume']
NUMERIC_COLUMNS = ['open', 'high', 'low', 'close', 'volume']


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the DataFrame schema and return rows that pass."""
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    df = df[EXPECTED_COLUMNS].copy()
    df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce')
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def split_valid_invalid(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a DataFrame into valid and invalid rows."""
    pass
