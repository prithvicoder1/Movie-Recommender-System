"""CineMatch: search a full movie catalogue and discover similar films."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from cinematch.artwork import MovieArtwork, TmdbCredentials, fetch_movie_artwork
from cinematch.catalogue import load_catalogue, movie_option_label, search_catalogue
from cinematch.presentation import feature_background, movie_card, safe
from cinematch.recommender import build_feature_matrix, recommend_movies
from cinematch.styles import APP_CSS


APP_DIR = Path(__file__).resolve().parent
MOVIE_LIST_PATH = APP_DIR / "movie_list.pkl"
METADATA_PATH = APP_DIR / "tmdb_5000_movies.csv"
RECOMMENDATION_COUNTS = [5, 10, 15, 20]


st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def read_secret(name: str) -> str | None:
    """Read a credential from the environment or untracked Streamlit secrets."""
    environment_value = os.getenv(name)
    if environment_value:
        return environment_value.strip()

    try:
        secret_value = st.secrets.get(name)
    except (FileNotFoundError, KeyError):
        secret_value = None
    return str(secret_value).strip() if secret_value else None


TMDB_CREDENTIALS = TmdbCredentials(
    bearer_token=read_secret("TMDB_BEARER_TOKEN"),
    api_key=read_secret("TMDB_API_KEY"),
)


@st.cache_resource(show_spinner=False)
def load_recommender() -> tuple[pd.DataFrame, Any]:
    """Load the complete catalogue and build its sparse recommendation index."""
    catalogue = load_catalogue(MOVIE_LIST_PATH, METADATA_PATH)
    return catalogue, build_feature_matrix(catalogue)


@st.cache_data(ttl=21_600, show_spinner=False)
def load_artwork_batch(
    movies: tuple[tuple[int, str, str], ...],
    _credentials: TmdbCredentials,
) -> dict[int, MovieArtwork]:
    """Fetch independent poster requests concurrently and cache the result."""
    if not _credentials.enabled or not movies:
        return {movie_id: MovieArtwork() for movie_id, _, _ in movies}

    def fetch(movie: tuple[int, str, str]) -> tuple[int, MovieArtwork]:
        movie_id, title, year = movie
        artwork = fetch_movie_artwork(movie_id, title, year, _credentials)
        return movie_id, artwork

    workers = min(8, len(movies))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return dict(executor.map(fetch, movies))


def attach_artwork(
    movies: list[dict[str, Any]],
    artwork_by_id: dict[int, MovieArtwork],
) -> list[dict[str, Any]]:
    """Attach poster and backdrop URLs without mutating catalogue rows."""
    enriched_movies: list[dict[str, Any]] = []
    for source_movie in movies:
        movie = dict(source_movie)
        artwork = artwork_by_id.get(int(movie["id"]), MovieArtwork())
        movie["poster_url"] = artwork.poster_url
        movie["backdrop_url"] = artwork.backdrop_url
        movie["artwork_error"] = artwork.error
        enriched_movies.append(movie)
    return enriched_movies


def activate_movie(movie_id: int) -> None:
    """Select a quick-pick movie and restore the full search catalogue."""
    st.session_state.active_movie_id = int(movie_id)
    st.session_state.movie_query = ""


catalogue, feature_matrix = load_recommender()
catalogue_by_id = catalogue.set_index("id", drop=False)
catalogue_count = len(catalogue)

interstellar_rows = catalogue.index[catalogue["title"].eq("Interstellar")]
default_movie_id = int(
    catalogue.loc[interstellar_rows[0], "id"]
    if not interstellar_rows.empty
    else catalogue.iloc[0]["id"]
)
if "active_movie_id" not in st.session_state:
    st.session_state.active_movie_id = default_movie_id
if "movie_query" not in st.session_state:
    st.session_state.movie_query = ""


st.markdown(APP_CSS, unsafe_allow_html=True)

artwork_status = (
    f"{catalogue_count:,} movies · live artwork"
    if TMDB_CREDENTIALS.enabled
    else f"{catalogue_count:,} movies · local mode"
)
st.markdown(
    f"""
    <nav class="nav">
        <div class="brand"><span class="brand-mark">C</span>CineMatch</div>
        <div class="nav-status"><span class="status-dot"></span>{artwork_status}</div>
    </nav>
    <section class="hero">
        <span class="eyebrow">✦ Search every story in the catalogue</span>
        <h1>Find the movie that <em>fits the mood.</em></h1>
        <p>Search {catalogue_count:,} films by title, original title, genre, or story.
        Then choose how deep you want the recommendations to go.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


with st.container(border=True):
    search_column, result_column = st.columns([1.05, 1.65])
    with search_column:
        query = st.text_input(
            "Search all movies",
            key="movie_query",
            placeholder="Try Interstellar, animation, space…",
        )

    search_results = search_catalogue(catalogue, query)
    result_ids = search_results["id"].astype(int).tolist()

    with result_column:
        if result_ids:
            active_movie_id = int(st.session_state.active_movie_id)
            selected_index = (
                result_ids.index(active_movie_id) if active_movie_id in result_ids else 0
            )
            selected_movie_id = st.selectbox(
                "Choose from the matching movies",
                options=result_ids,
                index=selected_index,
                format_func=lambda movie_id: movie_option_label(
                    catalogue_by_id.loc[int(movie_id)]
                ),
            )
        else:
            selected_movie_id = None
            st.selectbox(
                "Choose from the matching movies",
                options=["No movies match this search"],
                disabled=True,
            )

    depth_column, action_column = st.columns([1, 1.8])
    with depth_column:
        recommendation_count = st.selectbox(
            "Number of recommendations",
            options=RECOMMENDATION_COUNTS,
            index=1,
            format_func=lambda count: f"{count} movies",
        )
    with action_column:
        st.markdown("<div style='height:1.68rem'></div>", unsafe_allow_html=True)
        find_matches = st.button(
            "Find matching movies  →",
            type="primary",
            use_container_width=True,
            disabled=selected_movie_id is None,
        )

    match_count = len(search_results)
    summary = (
        f"<strong>{match_count:,}</strong> matching movies from the complete "
        f"<strong>{catalogue_count:,}-movie</strong> catalogue"
        if query.strip()
        else f"Browse the complete <strong>{catalogue_count:,}-movie</strong> catalogue"
    )
    st.markdown(f"<div class='search-summary'>{summary}</div>", unsafe_allow_html=True)

if find_matches and selected_movie_id is not None:
    st.session_state.active_movie_id = int(selected_movie_id)


st.markdown(
    "<div class='quick-label'>Or start with a crowd favourite</div>",
    unsafe_allow_html=True,
)
quick_pick_titles = ["The Dark Knight", "Avatar", "Toy Story", "The Matrix"]
quick_picks = catalogue[catalogue["title"].isin(quick_pick_titles)].drop_duplicates("title")
quick_pick_by_title = {row["title"]: int(row["id"]) for _, row in quick_picks.iterrows()}
quick_columns = st.columns(len(quick_pick_titles))
for quick_column, quick_title in zip(quick_columns, quick_pick_titles):
    with quick_column:
        movie_id = quick_pick_by_title.get(quick_title)
        if movie_id is not None:
            st.button(
                quick_title,
                key=f"quick-{movie_id}",
                use_container_width=True,
                on_click=activate_movie,
                args=(movie_id,),
            )


active_movie_id = int(st.session_state.active_movie_id)
active_movie = catalogue_by_id.loc[active_movie_id].to_dict()
recommendations = recommend_movies(
    catalogue,
    feature_matrix,
    active_movie_id,
    limit=int(recommendation_count),
)

artwork_records = tuple(
    (int(movie["id"]), str(movie["title"]), str(movie["year"]))
    for movie in [active_movie, *recommendations]
)
with st.spinner("Preparing posters and your cinematic banner…"):
    artwork_by_id = load_artwork_batch(artwork_records, TMDB_CREDENTIALS)

active_movie = attach_artwork([active_movie], artwork_by_id)[0]
recommendations = attach_artwork(recommendations, artwork_by_id)

if active_movie.get("artwork_error"):
    st.warning(
        f"{active_movie['artwork_error']} Recommendations still work from the local catalogue."
    )


genres = active_movie.get("genres_list") or []
runtime_value = float(active_movie.get("runtime") or 0)
runtime = f"{int(runtime_value)} min" if runtime_value > 0 else "Runtime n/a"
rating = float(active_movie.get("vote_average") or 0)
tagline = active_movie.get("tagline") or "A smart place to begin tonight."
banner_background = feature_background(active_movie)

st.markdown(
    f"""
    <div class="section-heading">
        <div><span>Tonight's starting point</span><h2>Your selection</h2></div>
        <p>Full-catalogue content matching · no watch history needed</p>
    </div>
    <section class="feature" style="background-image: {banner_background};">
        <div class="feature-copy">
            <span class="feature-kicker">Now exploring</span>
            <h2>{safe(active_movie['title'])}</h2>
            <p class="tagline">{safe(tagline)}</p>
            <p class="overview">{safe(active_movie['overview'])}</p>
            <div class="chips">
                <span class="chip">{safe(active_movie['year'])}</span>
                <span class="chip">★ {rating:.1f} / 10</span>
                <span class="chip">{runtime}</span>
                {''.join(f'<span class="chip">{safe(genre)}</span>' for genre in genres[:4])}
            </div>
        </div>
    </section>
    <div class="section-heading">
        <div>
            <span>{len(recommendations)} films, one shared DNA</span>
            <h2>Because you picked {safe(active_movie['title'])}</h2>
        </div>
        <p>Ranked from all {catalogue_count:,} available titles</p>
    </div>
    <section class="movie-grid">
        {''.join(movie_card(movie, rank) for rank, movie in enumerate(recommendations, start=1))}
    </section>
    """,
    unsafe_allow_html=True,
)


artwork_note = (
    "Posters and wide banners are supplied by TMDB."
    if TMDB_CREDENTIALS.enabled
    else "Configure a TMDB bearer token to replace local title art with live posters and banners."
)
st.markdown(
    f"<div class='footer-note'>Built for curious movie nights · {artwork_note} "
    "This product uses the TMDB API but is not endorsed or certified by TMDB.</div>",
    unsafe_allow_html=True,
)
