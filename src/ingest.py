"""Ingestion module.

Responsible for loading raw equities market data from CSV (or other sources)
into pandas DataFrames for downstream validation and transformation.
"""

import pandas as pd
import yaml
import logging

logger = logging.getLogger(__name__)


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    
    df = pd.read_csv(path)
    
    logger.info(f"Loaded {len(df)} rows from {path}")
    return df


def load_config(path: str) -> dict:
    """Load a YAML config file into a dictionary."""
    
    with open(path) as f:
        config = yaml.safe_load(f)

    logger.info(f"Loaded config from {path}")
    return config 
