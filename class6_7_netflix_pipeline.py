import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4:
    # Create a Path object from args.input.
    input_path = Path(args.input)
    # Inside a try block, load that path using pd.read_csv().
    try:
        df = pd.read_csv(input_path)
        df_original = df.copy()
    # Catch FileNotFoundError, log an ERROR message,
    except FileNotFoundError:
        logger.error(f'File not found: {input_path}')
    # and exit with sys.exit(1).
        sys.exit(1)
    # Log an INFO message.
    logger.info(f'Loaded {df.shape[0]} rows & {df.shape[1]} columns')


    # TODO 5:
    # Call show_overview().
    show_overview(df)
    # Log an INFO message.
    logger.info('Displayed DataFrame overview.')

    # TODO 6:
    # Call remove_duplicates().
    df, rows_removed = remove_duplicates(df)
    logger.info(f'Removed {rows_removed} duplicate row(s)')
    # Call drop_missing_rows().
    df, rows_removed = drop_missing_rows(df)
    logger.info(f'Dropped {rows_removed} rows with missing values')
    # Log an INFO message after each step that
    # includes the number of rows removed.

    # TODO 3:
    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).# Log an INFO message.

    try:
        df, iqr_removed = remove_iqr_outliers(df, 'runtime_minutes', 1.5)
        logger.info(f'Removed {iqr_removed} runtime_minutes outlier(s)')
    except ValueError as e:
        logger.info(f'Could not remove IQR outliers: {e}')
        sys.exit(1)
    # TODO 4:
    # Apply clean_text() to title, type, and country.
    for col in ['title','type','country']:
        df[col] = df[col].apply(clean_text)
        logger.info(f'Cleaned column: {col}')

    # TODO 5:
    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.

    report = {
        'rows_before': df_original.shape[0],
        'rows_after': df.shape[0],
        'rows_removed': (df_original.shape[0] - df.shape[0]),
        'columns': df.columns.to_list()
    }

    logger.info(report)

if __name__ == "__main__":
    main()