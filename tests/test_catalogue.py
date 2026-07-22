"""Regression tests for catalogue search and recommendation behavior."""

from __future__ import annotations

import unittest
from pathlib import Path

from cinematch.catalogue import load_catalogue, movie_option_label, search_catalogue
from cinematch.recommender import build_feature_matrix, recommend_movies


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = load_catalogue(
            PROJECT_ROOT / "movie_list.pkl",
            PROJECT_ROOT / "tmdb_5000_movies.csv",
        )

    def test_complete_catalogue_is_available_and_unique(self) -> None:
        self.assertEqual(len(self.catalogue), 4_800)
        self.assertEqual(self.catalogue["id"].nunique(), 4_800)

    def test_empty_search_returns_every_movie(self) -> None:
        results = search_catalogue(self.catalogue, "")
        self.assertEqual(len(results), len(self.catalogue))

    def test_title_search_ranks_exact_match_first(self) -> None:
        results = search_catalogue(self.catalogue, "Interstellar")
        self.assertGreater(len(results), 0)
        self.assertEqual(results.iloc[0]["title"], "Interstellar")

    def test_search_includes_genre_and_story_metadata(self) -> None:
        results = search_catalogue(self.catalogue, "animation")
        self.assertGreater(len(results), 20)

    def test_option_label_includes_year_rating_and_genre(self) -> None:
        movie = self.catalogue[self.catalogue["title"].eq("Interstellar")].iloc[0]
        label = movie_option_label(movie)
        self.assertIn("Interstellar (2014)", label)
        self.assertIn("★ 8.1", label)
        self.assertIn("Adventure", label)


class RecommendationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = load_catalogue(
            PROJECT_ROOT / "movie_list.pkl",
            PROJECT_ROOT / "tmdb_5000_movies.csv",
        )
        cls.feature_matrix = build_feature_matrix(cls.catalogue)

    def test_requested_recommendation_depth_is_respected(self) -> None:
        selected = self.catalogue[self.catalogue["title"].eq("Avatar")].iloc[0]
        recommendations = recommend_movies(
            self.catalogue,
            self.feature_matrix,
            int(selected["id"]),
            limit=20,
        )
        self.assertEqual(len(recommendations), 20)
        self.assertNotIn(int(selected["id"]), [movie["id"] for movie in recommendations])

    def test_unknown_movie_returns_no_recommendations(self) -> None:
        self.assertEqual(
            recommend_movies(self.catalogue, self.feature_matrix, -1, limit=10),
            [],
        )


if __name__ == "__main__":
    unittest.main()
