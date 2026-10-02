import logging
import re
import pandas as pd


logger = logging.getLogger(__name__)

def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    value = value.strip()
    # Convert text to lowercase.
    value = value.lower()
    # Collapse repeated whitespace.
    value = re.sub(r'\s+', ' ', value)
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    if column not in df.columns:
        logger.error(f'Column {column} not in dataframe')
        # Log an ERROR message and raise ValueError.
        raise ValueError(f'Column {column} not in dataframe')
    # Calculate Q1, Q3, and IQR.
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    # Use threshold to calculate lower and upper bounds.
    lower_bound = q1 - (iqr * threshold)
    upper_bound = q3 + (iqr * threshold)

    # Keep rows inside the bounds.
    previous_rows = len(df)
    df_iqr = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    rows_removed = previous_rows - len(df_iqr)
    # Log a DEBUG message containing the bounds and the number of rows removed.
    logger.debug(f'Lower bound: {lower_bound} | Upper bound: {upper_bound} | Removed rows: {rows_removed}')
    # Return the resulting DataFrame.
    return df_iqr, rows_removed

def show_overview(df):
    """Display basic information about a DataFrame."""
    # TODO 1:
    # Log a DEBUG message containing the shape.
    logger.debug(f'Dataframe Shape: {df.shape}')
    # Print the shape, first five rows, column names, and data types.
    print(f'Shape: {df.shape}')
    print(df.head(5))
    print(f'Columns: {list(df.columns)}')
    print(f'Data type: {df.info()}')


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # TODO 2:
    before_rows = len(df)
    # Remove exact duplicate rows.
    df = df.drop_duplicates()
    # Log a DEBUG message containing the before and after row counts.
    logger.debug(f'Before rows: {before_rows} | After rows: {df.shape[0]}')
    # Return the resulting DataFrame.
    rows_removed = before_rows - len(df)
    return df, rows_removed


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # TODO 3:
    before_rows = len(df)
    # Drop rows containing one or more missing values.
    df = df.dropna()
    # Log a DEBUG message containing the before and after row counts.
    logger.debug(f'Before rows: {before_rows} | After rows: {df.shape[0]}')
    # Return the resulting DataFrame.
    rows_removed = before_rows - len(df)
    return df, rows_removed