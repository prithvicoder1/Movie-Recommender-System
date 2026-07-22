"""Catalogue loading and full-dataset movie search."""

from __future__ import annotations

import json
import pickle
import re
from pathlib import Path
from typing import Any

import pandas as pd


METADATA_COLUMNS = [
    "id",
    "original_title",
    "original_language",
    "overview",
    "release_date",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "genres",
    "tagline",
]
TEXT_COLUMNS = [
    "title",
    "original_title",
    "overview",
    "release_date",
    "genres",
    "tagline",
    "tags",
]
DEFAULT_OVERVIEW = "A standout story waiting to be rediscovered."


def load_catalogue(movie_list_path: Path, metadata_path: Path) -> pd.DataFrame:
    """Load, validate, enrich, and de-duplicate the bundled movie catalogue."""
    with movie_list_path.open("rb") as model_file:
        tagged_movies = pickle.load(model_file)

    if not isinstance(tagged_movies, pd.DataFrame):
        raise TypeError("movie_list.pkl must contain a pandas DataFrame")

    required_tag_columns = {"id", "title", "tags"}
    missing_tag_columns = required_tag_columns.difference(tagged_movies.columns)
    if missing_tag_columns:
        missing = ", ".join(sorted(missing_tag_columns))
        raise ValueError(f"movie_list.pkl is missing columns: {missing}")

    metadata = pd.read_csv(metadata_path, usecols=METADATA_COLUMNS)
    catalogue = tagged_movies.merge(metadata, on="id", how="left", validate="many_to_one")

    # Some source rows were duplicated while joining the original credits file.
    # A stable movie ID is a better selector key than the title and keeps all
    # distinct films while removing accidental duplicates.
    catalogue = catalogue.drop_duplicates(subset="id", keep="first").copy()
    catalogue["id"] = catalogue["id"].astype(int)

    for column in TEXT_COLUMNS:
        catalogue[column] = catalogue[column].fillna("").astype(str)

    catalogue["overview"] = catalogue["overview"].replace("", DEFAULT_OVERVIEW)
    catalogue["year"] = catalogue["release_date"].str[:4].replace("", "—")
    catalogue["genres_list"] = catalogue["genres"].map(parse_genres)
    catalogue["search_text"] = catalogue.apply(_build_search_text, axis=1)

    numeric_defaults = {
        "runtime": 0.0,
        "vote_average": 0.0,
        "vote_count": 0,
        "popularity": 0.0,
    }
    for column, default in numeric_defaults.items():
        catalogue[column] = pd.to_numeric(catalogue[column], errors="coerce").fillna(default)

    return catalogue.reset_index(drop=True)


def parse_genres(raw_value: Any) -> list[str]:
    """Return genre names from the JSON stored in the TMDB CSV."""
    try:
        decoded = json.loads(raw_value or "[]")
        return [str(item["name"]) for item in decoded if item.get("name")]
    except (TypeError, ValueError, KeyError):
        return []


def search_catalogue(catalogue: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search every movie and rank strong title matches ahead of metadata matches.

    Empty queries intentionally return the entire catalogue. This keeps all
    bundled movies accessible instead of silently limiting the selector to a
    small curated subset.
    """
    normalized_query = _normalize(query)
    if not normalized_query:
        return catalogue.sort_values(
            ["popularity", "vote_count", "title"],
            ascending=[False, False, True],
            kind="stable",
        )

    title = catalogue["title"].map(_normalize)
    original_title = catalogue["original_title"].map(_normalize)
    search_text = catalogue["search_text"]

    exact = title.eq(normalized_query) | original_title.eq(normalized_query)
    starts_with = title.str.startswith(normalized_query) | original_title.str.startswith(
        normalized_query
    )
    title_contains = title.str.contains(normalized_query, regex=False) | original_title.str.contains(
        normalized_query, regex=False
    )
    metadata_contains = search_text.str.contains(normalized_query, regex=False)

    matched = catalogue.loc[title_contains | metadata_contains].copy()
    if matched.empty:
        return matched

    matched["_search_rank"] = 4
    matched.loc[metadata_contains & ~title_contains, "_search_rank"] = 3
    matched.loc[title_contains, "_search_rank"] = 2
    matched.loc[starts_with, "_search_rank"] = 1
    matched.loc[exact, "_search_rank"] = 0

    return matched.sort_values(
        ["_search_rank", "popularity", "vote_count", "title"],
        ascending=[True, False, False, True],
        kind="stable",
    ).drop(columns="_search_rank")


def movie_option_label(movie: pd.Series | dict[str, Any]) -> str:
    """Build a distinct, helpful label for a movie search result."""
    title = str(movie.get("title") or "Untitled")
    year = str(movie.get("year") or "—")
    rating = float(movie.get("vote_average") or 0)
    genres = movie.get("genres_list") or []
    genre = str(genres[0]) if genres else "Movie"
    return f"{title} ({year})  ·  ★ {rating:.1f}  ·  {genre}"


def _build_search_text(movie: pd.Series) -> str:
    genres = " ".join(parse_genres(movie.get("genres")))
    fields = [
        movie.get("title"),
        movie.get("original_title"),
        genres,
        movie.get("overview"),
        movie.get("tagline"),
    ]
    return _normalize(" ".join(str(field or "") for field in fields))


def _normalize(value: Any) -> str:
    """Normalize text for predictable, case-insensitive catalogue search."""
    return re.sub(r"\s+", " ", str(value or "").casefold()).strip()
