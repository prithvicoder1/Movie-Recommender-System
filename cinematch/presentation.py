"""Small HTML presentation helpers for the Streamlit interface."""

from __future__ import annotations

import hashlib
import html
from typing import Any


def safe(value: Any) -> str:
    """Escape dynamic values before inserting them into HTML or CSS."""
    return html.escape(str(value or ""), quote=True)


def gradient_for(title: str) -> str:
    """Return stable fallback artwork colors for a title."""
    palettes = [
        ("#ff5c35", "#7b1cff"),
        ("#00b8a9", "#103e8c"),
        ("#f2c94c", "#b620e0"),
        ("#ff3d77", "#4320a8"),
        ("#36d1dc", "#5b2cff"),
        ("#ef4444", "#172554"),
    ]
    digest = hashlib.sha256(title.encode("utf-8")).hexdigest()
    start, end = palettes[int(digest, 16) % len(palettes)]
    return f"linear-gradient(145deg, {start} 0%, {end} 100%)"


def feature_background(movie: dict[str, Any]) -> str:
    """Create a readable banner background, preferring a wide TMDB backdrop."""
    image_url = movie.get("backdrop_url") or movie.get("poster_url")
    fallback = gradient_for(str(movie.get("title") or "Movie"))
    if not image_url:
        return fallback

    return (
        "linear-gradient(90deg, rgba(8,9,14,.98) 0%, rgba(8,9,14,.88) 43%, "
        "rgba(8,9,14,.28) 78%, rgba(8,9,14,.42) 100%), "
        f"url('{safe(image_url)}')"
    )


def movie_card(movie: dict[str, Any], rank: int) -> str:
    """Render one ranked recommendation card with a resilient art fallback."""
    title = safe(movie.get("title"))
    genres = " · ".join(movie.get("genres_list") or ["Cinema"])
    rating = float(movie.get("vote_average") or 0)
    poster_url = movie.get("poster_url")

    if poster_url:
        art_style = (
            "background-image: linear-gradient(180deg, transparent 54%, "
            f"rgba(7,8,13,.96) 100%), url('{safe(poster_url)}');"
        )
        fallback = ""
    else:
        art_style = f"background-image: {gradient_for(str(movie.get('title')))};"
        fallback = (
            "<div class='fallback-art'>"
            f"<span>{safe(genres)}</span><strong>{title}</strong>"
            "<small>CINEMATCH SELECT</small></div>"
        )

    match_percent = max(1, round(float(movie.get("similarity") or 0) * 100))
    return f"""
    <article class="movie-card">
        <div class="movie-poster" style="{art_style}">
            <span class="rank-badge">{rank:02d}</span>
            {fallback}
            <span class="match-badge">MATCH {match_percent}%</span>
        </div>
        <div class="movie-copy">
            <h3 title="{title}">{title}</h3>
            <div class="movie-meta">
                <span>{safe(movie.get('year') or '—')}</span>
                <span class="dot"></span>
                <span>★ {rating:.1f}</span>
            </div>
            <p>{safe(genres)}</p>
        </div>
    </article>
    """
