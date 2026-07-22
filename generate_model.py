"""Regenerate the tagged movie catalogue from the original TMDB CSV files.

The application builds its sparse TF-IDF matrix at runtime, so this script only
creates ``movie_list.pkl``. It intentionally avoids generating or committing a
large dense similarity matrix.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
from typing import Any

import pandas as pd


def parse_named_items(raw_value: str) -> list[str]:
    """Extract normalized names from a TMDB JSON-like list."""
    return [
        str(item["name"]).replace(" ", "")
        for item in ast.literal_eval(raw_value)
        if item.get("name")
    ]


def parse_directors(raw_value: str) -> list[str]:
    """Extract director names from a TMDB crew list."""
    return [
        str(item["name"]).replace(" ", "")
        for item in ast.literal_eval(raw_value)
        if item.get("job") == "Director" and item.get("name")
    ]


def build_tagged_catalogue(movies_path: Path, credits_path: Path) -> pd.DataFrame:
    """Combine movie metadata and credits into the app's tagged-data schema."""
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    merged = movies.merge(
        credits,
        left_on=["id", "title"],
        right_on=["movie_id", "title"],
        how="inner",
        validate="one_to_one",
    )

    columns = ["id", "title", "overview", "genres", "keywords", "cast", "crew"]
    tagged = merged[columns].dropna().copy()
    tagged["overview"] = tagged["overview"].map(str.split)
    tagged["genres"] = tagged["genres"].map(parse_named_items)
    tagged["keywords"] = tagged["keywords"].map(parse_named_items)
    tagged["cast"] = tagged["cast"].map(parse_named_items).map(lambda names: names[:3])
    tagged["crew"] = tagged["crew"].map(parse_directors)

    feature_columns = ["overview", "genres", "keywords", "cast", "crew"]
    tagged["tags"] = tagged[feature_columns].apply(
        lambda row: " ".join(
            str(token).casefold()
            for values in row
            for token in _as_list(values)
        ),
        axis=1,
    )
    return tagged[["id", "title", "tags"]].drop_duplicates("id").reset_index(drop=True)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--movies", type=Path, default=Path("tmdb_5000_movies.csv"))
    parser.add_argument("--credits", type=Path, default=Path("tmdb_5000_credits.csv"))
    parser.add_argument("--output", type=Path, default=Path("movie_list.pkl"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for source in (args.movies, args.credits):
        if not source.is_file():
            raise FileNotFoundError(f"Required dataset not found: {source}")

    catalogue = build_tagged_catalogue(args.movies, args.credits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    catalogue.to_pickle(args.output)
    print(f"Saved {len(catalogue):,} tagged movies to {args.output}")


if __name__ == "__main__":
    main()
