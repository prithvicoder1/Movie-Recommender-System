"""Tests for secure TMDB artwork lookup and fallback behavior."""

from __future__ import annotations

import unittest

from cinematch.artwork import TmdbCredentials, fetch_movie_artwork


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self.payload


class FakeSession:
    def __init__(self, payloads: list[dict[str, object]]) -> None:
        self.payloads = list(payloads)
        self.calls: list[dict[str, object]] = []

    def get(self, url: str, **kwargs: object) -> FakeResponse:
        self.calls.append({"url": url, **kwargs})
        return FakeResponse(self.payloads.pop(0))


class ArtworkTests(unittest.TestCase):
    def test_no_credentials_skips_network(self) -> None:
        session = FakeSession([])
        artwork = fetch_movie_artwork(
            157336,
            "Interstellar",
            "2014",
            TmdbCredentials(),
            session=session,
        )
        self.assertEqual(artwork.poster_url, "")
        self.assertEqual(session.calls, [])

    def test_details_lookup_builds_poster_and_backdrop_urls(self) -> None:
        session = FakeSession(
            [{"poster_path": "/poster.jpg", "backdrop_path": "/backdrop.jpg"}]
        )
        artwork = fetch_movie_artwork(
            157336,
            "Interstellar",
            "2014",
            TmdbCredentials(bearer_token="secret-token"),
            session=session,
        )
        self.assertTrue(artwork.poster_url.endswith("/w500/poster.jpg"))
        self.assertTrue(artwork.backdrop_url.endswith("/w1280/backdrop.jpg"))
        headers = session.calls[0]["headers"]
        self.assertEqual(headers["Authorization"], "Bearer secret-token")

    def test_search_fills_missing_backdrop(self) -> None:
        session = FakeSession(
            [
                {"poster_path": "/poster.jpg", "backdrop_path": None},
                {"results": [{"poster_path": None, "backdrop_path": "/wide.jpg"}]},
            ]
        )
        artwork = fetch_movie_artwork(
            1,
            "Example",
            "2001",
            TmdbCredentials(api_key="secret-key"),
            session=session,
        )
        self.assertTrue(artwork.poster_url.endswith("/w500/poster.jpg"))
        self.assertTrue(artwork.backdrop_url.endswith("/w1280/wide.jpg"))
        self.assertEqual(session.calls[1]["params"]["year"], "2001")
        self.assertEqual(session.calls[1]["params"]["api_key"], "secret-key")


if __name__ == "__main__":
    unittest.main()
