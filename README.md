# equities-market-data-tool

A data pipeline that ingests, validates, transforms, and reports on equities market price data. Raw CSV input is checked for schema and business-rule violations; clean rows are enriched with derived metrics (e.g. moving averages, returns) and summarised, while rejected rows are written to an errors directory for review.

## Setup

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (bash / Git Bash)
source .venv/Scripts/activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

_TBD — pipeline entry point will be `python -m src.main` driven by `config.yaml`._

## Project Structure

```
equities-market-data-tool/
├── data/
│   ├── raw/           # Source CSVs (e.g. market_prices.csv)
│   ├── processed/     # Cleaned, transformed outputs
│   └── errors/        # Rejected rows from validation
├── src/
│   ├── __init__.py
│   ├── ingest.py      # CSV / config loading
│   ├── validate.py    # Schema and business-rule checks
│   ├── transform.py   # Derived columns (moving avg, returns)
│   ├── report.py      # Summaries and output writers
│   └── main.py        # Pipeline entry point
├── tests/
│   ├── __init__.py
│   └── test_functions.py
├── scripts/
│   └── generate_sample_data.py  # Synthetic dataset generator
├── .gitignore
├── requirements.txt
├── README.md
└── config.yaml        # Paths and pipeline parameters
```
