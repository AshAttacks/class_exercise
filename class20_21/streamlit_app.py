import logging

import pandas as pd
import requests
import streamlit as st

from api_client import fetch_records

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

st.title("Movie Explorer")
st.write("Explore genre summaries and yearly rating trends.")

st.header("Which genres have the highest average ratings?")
min_movies = st.slider("Minimum movies per genre", 1, 6, 3)

try:
    records = fetch_records("/analysis/genres", {"min_movies": min_movies})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve genre summary: {error}")
    st.error("Cannot load genre data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No genres match this minimum movie count.")
else:
    genre_df = pd.DataFrame(records)
    st.dataframe(genre_df, hide_index=True)
    st.bar_chart(genre_df, x="genre", y="average_rating")
    logger.info(f"Displayed genre summary: groups={len(genre_df)}")

st.header("How have ratings changed over time?")
window = st.slider("Rolling window (yearly observations)", 1, 6, 3)

# TODO: Request /analysis/years with window as a query parameter.
# Catch requests.RequestException and show an error, then call st.stop().
# If the returned list is empty, show an informational message.
# Otherwise, create a DataFrame and display its table.
# Show a line chart with release_year on the x-axis and
# average_rating and rolling_rating as the two lines.
# Log the year count and selected window at INFO.

try:
    records = fetch_records("/analysis/years", {"window": window})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve year trend: {error}")
    st.error("Cannot load year data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No genres match this minimum movie count.")
else:
    year_df = pd.DataFrame(records)
    st.dataframe(year_df, hide_index=True)
    st.header("Two lines: compare trends")
    st.line_chart(
        year_df,
        x="release_year",
        y=["average_rating", "rolling_rating"],
    )
    logger.info(f"Displayed year trend: groups={len(year_df)}")

st.header("Which movies meet your minimum rating?")
min_rating = st.slider("Minimum movie rating", 0.0, 10.0, 8.0, 0.5)

# TODO: Use fetch_records() to request /movies/filter with min_rating.
# Catch requests.RequestException, show an error, and call st.stop().
# If the list is empty, show an informational message.
# Otherwise, display the returned records as a DataFrame table.
# Log the displayed row count and minimum rating at INFO.

try:
    records = fetch_records("/movies/filter", {"min_rating": min_rating})
except requests.RequestException as error:
    logger.warning(f"Cannot retrieve records: {error}")
    st.error("Cannot load filtered data. Check that the API is running.")
    st.stop()

if not records:
    st.info("No records match this minimum rating.")
else:
    filtered = pd.DataFrame(records)
    st.dataframe(filtered, hide_index=True)
    logger.info(f"Row count: groups={len(filtered)} | Minimum Rating = {min_rating}")

