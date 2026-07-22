"""Sparse content-based recommendation engine."""

from __future__ import annotations

from typing import Any

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def build_feature_matrix(catalogue: pd.DataFrame) -> csr_matrix:
    """Create a compact feature matrix from the preprocessed movie tags."""
    vectorizer = TfidfVectorizer(
        max_features=8_000,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )
    return vectorizer.fit_transform(catalogue["tags"].fillna(""))


def recommend_movies(
    catalogue: pd.DataFrame,
    feature_matrix: csr_matrix,
    movie_id: int,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return the closest movies for one stable TMDB movie ID."""
    if limit < 1:
        return []

    selected_rows = catalogue.index[catalogue["id"].eq(int(movie_id))]
    if selected_rows.empty:
        return []

    selected_index = int(selected_rows[0])
    scores = linear_kernel(feature_matrix[selected_index], feature_matrix).ravel()
    ranked_indices = scores.argsort()[::-1]

    recommendations: list[dict[str, Any]] = []
    for raw_index in ranked_indices:
        index = int(raw_index)
        if index == selected_index:
            continue

        movie = catalogue.iloc[index].to_dict()
        movie["similarity"] = float(scores[index])
        recommendations.append(movie)
        if len(recommendations) == limit:
            break

    return recommendations
