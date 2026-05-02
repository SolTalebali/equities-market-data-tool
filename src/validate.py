"""Validation module.

Provides functions to check ingested market data for schema correctness,
type validity, and business-rule violations (e.g. high >= low, non-negative
prices and volume).
"""

import pandas as pd


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the DataFrame schema and return rows that pass."""
    pass


def split_valid_invalid(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a DataFrame into valid and invalid rows."""
    pass
