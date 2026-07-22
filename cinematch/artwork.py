"""Secure TMDB artwork retrieval with poster and backdrop fallbacks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TMDB_API_ROOT = "https://api.themoviedb.org/3"
TMDB_IMAGE_ROOT = "https://image.tmdb.org/t/p"


@dataclass(frozen=True)
class TmdbCredentials:
    """TMDB authentication values loaded from secrets or the environment."""

    bearer_token: str | None = None
    api_key: str | None = None

    @property
    def enabled(self) -> bool:
        return bool(self.bearer_token or self.api_key)


@dataclass(frozen=True)
class MovieArtwork:
    """Artwork URLs and a safe diagnostic for the UI."""

    poster_url: str = ""
    backdrop_url: str = ""
    error: str = ""


class ArtworkRequestError(Exception):
    """Normalized HTTP failure that never includes a credential or request URL."""

    def __init__(self, status_code: int | None = None) -> None:
        super().__init__("TMDB artwork request failed")
        self.status_code = status_code


def fetch_movie_artwork(
    movie_id: int,
    title: str,
    year: str,
    credentials: TmdbCredentials,
    *,
    session: Any | None = None,
) -> MovieArtwork:
    """Fetch a movie poster and wide backdrop without exposing credentials.

    TMDB ID lookup is authoritative. A title/year search is used only when the
    old dataset ID no longer resolves or the returned record lacks artwork.
    """
    if not credentials.enabled:
        return MovieArtwork()

    try:
        details = _get_json(
            f"{TMDB_API_ROOT}/movie/{int(movie_id)}",
            credentials,
            {"language": "en-US"},
            session,
        )

        if not (details.get("poster_path") and details.get("backdrop_path")):
            search_params: dict[str, str] = {
                "query": title,
                "include_adult": "false",
                "language": "en-US",
                "page": "1",
            }
            if year and year != "—":
                search_params["year"] = year

            search_payload = _get_json(
                f"{TMDB_API_ROOT}/search/movie",
                credentials,
                search_params,
                session,
            )
            candidates = search_payload.get("results") or []
            if candidates:
                candidate = candidates[0]
                details = {
                    "poster_path": details.get("poster_path")
                    or candidate.get("poster_path"),
                    "backdrop_path": details.get("backdrop_path")
                    or candidate.get("backdrop_path"),
                }

        return MovieArtwork(
            poster_url=_image_url("w500", details.get("poster_path")),
            backdrop_url=_image_url("w1280", details.get("backdrop_path")),
        )
    except ArtworkRequestError as error:
        if error.status_code == 401:
            return MovieArtwork(error="TMDB rejected the configured credential.")
        if error.status_code == 404:
            return MovieArtwork()
        return MovieArtwork(error="TMDB artwork is temporarily unavailable.")
    except (TypeError, ValueError):
        return MovieArtwork(error="TMDB artwork is temporarily unavailable.")


def _get_json(
    url: str,
    credentials: TmdbCredentials,
    params: dict[str, str],
    session: Any | None,
) -> dict[str, Any]:
    headers = {"accept": "application/json"}
    request_params = dict(params)
    if credentials.bearer_token:
        headers["Authorization"] = f"Bearer {credentials.bearer_token}"
    elif credentials.api_key:
        request_params["api_key"] = credentials.api_key

    if session is not None:
        response = session.get(
            url,
            headers=headers,
            params=request_params,
            timeout=8,
        )
        try:
            response.raise_for_status()
        except Exception as error:
            response_status = getattr(getattr(error, "response", None), "status_code", None)
            raise ArtworkRequestError(response_status) from error
        payload = response.json()
    else:
        request_url = f"{url}?{urlencode(request_params)}"
        request = Request(request_url, headers=headers)
        try:
            with urlopen(request, timeout=8) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise ArtworkRequestError(error.code) from error
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise ArtworkRequestError() from error

    return payload if isinstance(payload, dict) else {}


def _image_url(size: str, path: Any) -> str:
    return f"{TMDB_IMAGE_ROOT}/{size}{path}" if path else ""
