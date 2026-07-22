"""Core services for the CineMatch Streamlit application."""

from .catalogue import load_catalogue, movie_option_label, search_catalogue
from .recommender import build_feature_matrix, recommend_movies

__all__ = [
    "build_feature_matrix",
    "load_catalogue",
    "movie_option_label",
    "recommend_movies",
    "search_catalogue",
]
