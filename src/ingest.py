import pandas as pd
import yaml
import logging

logger = logging.getLogger(__name__)


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    logger.info(f"Loaded {len(df)} rows from {path}")
    return df


def load_config(path: str) -> dict:
    """Load a YAML config file into a dictionary."""
    
    with open(path) as f:
        config = yaml.safe_load(f)

    logger.info(f"Loaded config from {path}")
    return config