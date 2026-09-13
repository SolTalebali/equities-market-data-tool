import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Generates a per-ticker summary DataFrame."""

    result = df.groupby('ticker').agg(
        mean_daily_return=('daily_return', "mean"),
        mean_spread=('spread', "mean"),
        total_volume=('volume', "sum"),
    ).reset_index()

    logger.info(f"summarized {len(result)} tickers")
    return result


def write_processed(df: pd.DataFrame, path: str) -> None:

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

    logger.info(f"Wrote {len(df)} rows to {path}")


def write_errors(df: pd.DataFrame, path: str) -> None:

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

    logger.info(f"Wrote {len(df)} rows to {path}")
