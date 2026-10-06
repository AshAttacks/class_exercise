import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_cols):
    """Check that all required columns exist."""
    # TODO 2:
    # Check if any of the configured columns (list) are missing from df.

    missing_columns = [col for col in required_cols if col not in df.columns]
    if missing_columns:
        logger.error(f'{len(missing_columns)} columns missing.')
        raise ValueError(f'{len(missing_columns)} columns missing.')

    # If any are missing, log an ERROR and raise ValueError.
    logger.info('Required columns are present')
    # Log an INFO.
    # Return the DataFrame.
    return df