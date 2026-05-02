"""Reporting module.

Produces summary outputs from the transformed data, including per-ticker
statistics and writes processed/error datasets to disk.
"""

import pandas as pd


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a per-ticker summary DataFrame."""
    pass


def write_processed(df: pd.DataFrame, path: str) -> None:
    """Write the processed DataFrame to disk."""
    pass


def write_errors(df: pd.DataFrame, path: str) -> None:
    """Write rejected rows to the errors directory."""
    pass
