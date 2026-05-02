"""Ingestion module.

Responsible for loading raw equities market data from CSV (or other sources)
into pandas DataFrames for downstream validation and transformation.
"""

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    pass


def load_config(path: str) -> dict:
    """Load a YAML config file into a dictionary."""
    pass
