import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

from check_analysis import summarize_genres, summarize_years

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie Analysis API")
df = pd.read_csv(Path("data") / "class20_movies.csv")

@app.get("/analysis/genres", response_model=list[dict])
def get_genres(min_movies: int = Query(default=1, ge=1)):
    # TODO: Pass min_movies to summarize_genres().
    summarize = summarize_genres(df, min_movies=min_movies)
    # Log the number of groups at INFO and return records.
    logger.info(f"Returned {summarize['movie_count'].sum()} Records & {len(summarize)} Groups")
    return summarize.to_dict(orient="records")

@app.get("/analysis/years", response_model=list[dict])
def get_years(window: int = Query(default=3, ge=1)):
    # TODO: Call summarize_years() with window.
    summarize = summarize_years(df, window=window)
    # Log the year count and window at INFO and return records.
    logger.info(f'Returned {summarize['release_year'].count()} years '
                f'and {len(summarize['release_year'])} records')
    return summarize.to_dict(orient="records")