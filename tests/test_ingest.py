import pandas as pd
from src.ingest import load_csv, load_config


def test_load_csv(tmp_path):
    path = tmp_path / "sample.csv"
    path.write_text("a,b\n1,x\n2,y\n")
    df = load_csv(str(path))

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b"]


def test_load_config(tmp_path):
    path = tmp_path / "sample_config.yaml"
    path.write_text("input_path: data/sample.csv\nmoving_average_window: 5")
    config = load_config(str(path))
    
    assert config == {"input_path" : "data/sample.csv", "moving_average_window": 5}