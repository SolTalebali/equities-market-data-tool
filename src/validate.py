"""Validation module.

Provides functions to check ingested market data for schema correctness,
type validity, and business-rule violations (e.g. high >= low, non-negative
prices and volume).
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

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
    
    logger.info("Validated schema")
    return df


def split_valid_invalid(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a DataFrame into valid and invalid rows."""

    df = df.copy()
    df["reason"] = ""

    df.loc[df["volume"] < 0, "reason"] += "Negative volume; "
    df.loc[df["high"] < df["low"], "reason"] += "High less than low; "
    df.loc[df["high"] < df["open"], "reason"] += "High less than open; "
    df.loc[df["high"] < df["close"], "reason"] += "High less than close; "
    df.loc[df["low"] > df["open"], "reason"] += "Low greater than open; "
    df.loc[df["low"] > df["close"], "reason"] += "Low greater than close; " 
    df.loc[df[NUMERIC_COLUMNS].isna().any(axis=1), "reason"] += "Missing or non-numeric value; "
    df.loc[(df[["open", "high", "low", "close"]] < 0).any(axis=1), "reason"] += "Negative price; "
    df.loc[df["ticker"].isna(), "reason"] += "Missing ticker; "
    df.loc[df["trade_date"].isna(), "reason"] += "Missing or invalid trade_date; "
    
    valid_df = df[df["reason"] == ""].drop(columns="reason")
    invalid_df = df[df["reason"] != ""]

    logger.info(f"Validated: {len(valid_df)} valid, {len(invalid_df)} invalid")
    return valid_df, invalid_df
