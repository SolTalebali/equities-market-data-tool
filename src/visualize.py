"""Visualization module.

Generates per-ticker charts (close price + moving average overlay) from
transformed market data. Charts are written to disk as PNG files.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


logger = logging.getLogger(__name__)


def plot_close_with_moving_average(df: pd.DataFrame, output_dir: str, window: int) -> None:
    """Save one PNG per ticker showing close price and moving average."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ma_col = f"moving_average_{window}"

    for ticker, group in df.groupby("ticker"):
        plt.figure(figsize=(10, 6))
        plt.plot(group["trade_date"], group["close"], label="close")
        plt.plot(group["trade_date"], group[ma_col], label=f"{window}-day MA")
        plt.title(f"{ticker} close price")
        plt.xlabel("Date")
        plt.ylabel("price")
        plt.legend()
        plt.savefig(output_dir / f"{ticker}.png")
        plt.close()

    logger.info(f"Saved {df['ticker'].nunique()} charts to {output_dir}")