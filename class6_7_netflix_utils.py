import logging

logger = logging.getLogger(__name__)


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