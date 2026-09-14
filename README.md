# equities-market-data-tool

A data pipeline that ingests, validates, transforms, and reports on daily equities market price data. Raw CSV input is checked for schema and business-rule violations; clean rows are enriched with derived analytics (daily return, spread, moving averages, volume change) and summarised per ticker, while rejected rows are written to an errors directory with the reason for rejection.

## Setup

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv

# Windows (Git Bash)
source .venv/Scripts/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Run the full pipeline:

```bash
python -m src.main
```

Run it from the project root, since paths in `config.yaml` are relative. Use the `-m` form: running `python src/main.py` directly fails with `ModuleNotFoundError: No module named 'src'`.

This reads `config.yaml`, processes the input CSV, and writes:

- `data/processed/processed.csv` — clean rows with all derived analytics
- `data/processed/summary.csv` — per-ticker aggregate stats
- `data/processed/charts/<TICKER>.png` — one close price + moving average chart per ticker
- `data/errors/errors.csv` — rejected rows with a `reason` column explaining why each was excluded
- `logs/pipeline.log` — timestamped log of pipeline events

## Configuration

All paths and parameters are driven by `config.yaml`:

```yaml
input_path: data/raw/market_prices.csv
output_path: data/processed/
error_path: data/errors/
log_path: logs/pipeline.log
moving_average_window: 5
```

| Key | Description |
|---|---|
| `input_path` | Raw input CSV consumed by the ingest stage |
| `output_path` | Directory for processed rows, the summary, and charts |
| `error_path` | Directory for rejected rows |
| `log_path` | Log file location; its parent directory is created if missing |
| `moving_average_window` | Window size, in trading days, for the moving average |

## Pipeline Stages

| Stage | Module | Responsibility |
|---|---|---|
| Ingest | `src/ingest.py` | Load the raw CSV and YAML config |
| Validate | `src/validate.py` | Enforce schema (required columns, type coercion) and split rows into valid / invalid based on business rules |
| Transform | `src/transform.py` | Add derived columns (`daily_return`, `spread`, `volume_change`, `moving_average_<window>`) |
| Report | `src/report.py` | Summarise per-ticker stats and write CSV outputs |
| Visualise | `src/visualize.py` | Generate per-ticker close price + moving average charts as PNG files |
| Orchestration | `src/main.py` | Wire the stages together end-to-end |

### Validation rules

Rows are rejected if any of the following hold:

- Negative volume
- Negative price (any of `open`, `high`, `low`, `close`)
- `high < low`, `high < open`, `high < close`, `low > open`, `low > close`
- Missing or non-numeric value in any numeric column
- Missing ticker
- Missing or invalid `trade_date`

Each rejected row carries a `reason` column listing every rule it violated.

### Derived columns

Valid rows are sorted by `ticker` and `trade_date`, and every calculation that looks at previous rows is done per ticker.

| Column | Definition |
|---|---|
| `daily_return` | `(close - previous close) / previous close`, as a fraction (`0.10` = 10%) |
| `spread` | `high - low` |
| `volume_change` | `(volume - previous volume) / previous volume`, as a fraction |
| `moving_average_<window>` | Rolling mean of `close` over the last `<window>` rows |

`daily_return` and `volume_change` are empty on each ticker's first row. `moving_average_<window>` is empty on each ticker's first `<window> - 1` rows.

### Summary columns

`summary.csv` has one row per ticker:

| Column | Definition |
|---|---|
| `mean_daily_return` | Mean of `daily_return` |
| `mean_spread` | Mean of `spread` |
| `total_volume` | Sum of `volume` |

## Testing

Run the test suite with pytest:

```bash
pytest
```

Tests live under `tests/`, one file per source module. They build small DataFrames in memory, or write temporary files with pytest's `tmp_path`, rather than depending on the sample CSV or `config.yaml`, so they're isolated and fast.

Run a single test with:

```bash
pytest tests/test_ingest.py::test_load_config
```

## Project Structure

```
equities-market-data-tool/
├── data/
│   ├── raw/           # Source CSVs
│   ├── processed/     # Cleaned + transformed output and charts/ (gitignored)
│   └── errors/        # Rejected rows (gitignored)
├── logs/              # Pipeline logs (gitignored)
├── src/
│   ├── __init__.py
│   ├── ingest.py
│   ├── validate.py
│   ├── transform.py
│   ├── report.py
│   ├── visualize.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_ingest.py
│   ├── test_validate.py
│   ├── test_transform.py
│   └── test_report.py
├── scripts/
│   └── generate_sample_data.py   # Synthetic dataset generator
├── config.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## Tech Stack

- Python 3.12
- pandas — DataFrame manipulation, groupby, rolling windows
- PyYAML — config loading
- pytest — test framework
- Matplotlib — per-ticker price charts

## Possible Extensions

Stretch ideas not implemented in the foundation version:

- CLI arguments to override config values at runtime (e.g. `--config`, `--window`)
- SQLite output as an alternative to CSV
- FastAPI endpoint exposing the pipeline as a service
- Docker packaging for portable deployment
