"""Tests for the ingest module."""

import pandas as pd

from src.ingest import load_csv, load_config


def test_load_csv():
    """Test that load_csv correctly loads a CSV file into a DataFrame."""
    df = load_csv("data/raw/market_prices.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["ticker", "trade_date", "open", "high", "low", "close", "volume"]


def test_load_config():
    """Test that load_config correctly loads a YAML config file into a dictionary."""
    config = load_config("config.yaml")
    assert isinstance(config, dict)
    assert "input_path" in config
    assert isinstance(config["input_path"], str)