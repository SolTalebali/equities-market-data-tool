"""Pipeline entry point.

Wires together ingest, validate, transform, and report stages into a single
end-to-end run driven by config.yaml.
"""

import logging
from pathlib import Path

from src.ingest import load_csv, load_config
from src.validate import validate_schema, split_valid_invalid
from src.transform import add_daily_return, add_moving_average, add_spread, add_volume_change
from src.report import summarize, write_errors, write_processed
from src.visualize import plot_close_with_moving_average

logger = logging.getLogger(__name__)


def run() -> None:
    """Run the end-to-end pipeline."""

    config = load_config("config.yaml")
    log_path = Path(config["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(),
        ]
    )

    logger.info("Pipeline starting")
    
    df = load_csv(config["input_path"])
    df = validate_schema(df)
    valid, invalid = split_valid_invalid(df)

    valid = add_daily_return(valid)
    valid = add_moving_average(valid, window=config["moving_average_window"])
    valid = add_spread(valid)
    valid = add_volume_change(valid)

    plot_close_with_moving_average(valid, config["output_path"] + "charts/", config["moving_average_window"])

    write_processed(valid, config["output_path"] + "processed.csv")
    write_errors(invalid, config["error_path"] + "errors.csv")
    summary = summarize(valid)
    write_processed(summary, config["output_path"] + "summary.csv")

    logger.info("Pipeline complete")


if __name__ == "__main__":
    run()
