<div align="center">

# 🎬 CineMatch

### A polished, story-first movie recommendation experience.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![TMDB](https://img.shields.io/badge/TMDB-optional_live_artwork-01B4E4?style=flat-square)](https://www.themoviedb.org/)

Search the complete bundled catalogue and get 5–20 recommendations that share
a movie's themes, genres, cast, and creative DNA. The recommendation engine runs
locally; TMDB credentials securely enable live posters and wide hero banners.

</div>

## What changed

- Full-catalogue search across 4,800 unique movies by title, original title,
  genre, and story metadata—no small curated search subset.
- Adjustable recommendation depth: 5, 10, 15, or 20 ranked movies.
- A cinematic, responsive interface with quick picks, detailed ratings,
  high-resolution poster cards, and a backdrop-style selected-movie banner.
- A self-contained TF-IDF recommendation index built from the included data, so
  the project no longer depends on a missing `similarity.pkl` file.
- Secure TMDB configuration through Streamlit secrets or environment variables.
  No API key is stored in the repository.
- TMDB ID lookup plus a title/year recovery lookup when older records lack art.
- A graceful local mode with generated title art when TMDB is not configured.
- Cached, concurrent artwork requests for fast repeat interactions.
- Separated catalogue, recommendation, artwork, presentation, and styling
  modules with regression tests for the core behavior.

## How it works

1. The app loads 4,800 unique tagged movies from `movie_list.pkl`.
2. The search service ranks matches from the complete local catalogue.
3. `TfidfVectorizer` converts movie tags into a sparse feature matrix.
4. A query-time cosine comparison ranks up to 20 closest titles.
5. Local CSV metadata supplies year, runtime, rating, genres, and overview.
6. If configured, TMDB supplies live posters and wide backdrops.

This keeps startup lightweight and avoids committing a large dense similarity
matrix to Git.

## Run locally

```bash
git clone https://github.com/prithvicoder1/Movie-Recommender-System.git
cd Movie-Recommender-System

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501). Search and recommendations
work immediately without an external API; local title artwork is used until a
TMDB credential is configured.

## Enable TMDB artwork securely

Create a free API credential from [TMDB account settings](https://www.themoviedb.org/settings/api).
The read access token is preferred over embedding a v3 key in a request URL.

### Streamlit secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then place the real token in `.streamlit/secrets.toml`:

```toml
TMDB_BEARER_TOKEN = "your_read_access_token"
```

### Environment variable

```bash
export TMDB_BEARER_TOKEN="your_read_access_token"
streamlit run app.py
```

Legacy `TMDB_API_KEY` values are also supported. Both `.streamlit/secrets.toml`
and `.env` are git-ignored. Never commit a real credential.

For Streamlit Community Cloud, add `TMDB_BEARER_TOKEN` in the app's **Settings →
Secrets** panel, then reboot the app. GitHub repository secrets are not exposed
to Streamlit automatically.

## Project structure

```text
.
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── cinematch/
│   ├── artwork.py            # Secure poster/backdrop retrieval
│   ├── catalogue.py          # Loading, cleanup, and full search
│   ├── presentation.py       # Safe movie-card HTML helpers
│   ├── recommender.py        # Sparse TF-IDF ranking
│   └── styles.py             # Responsive visual system
├── tests/
│   ├── test_artwork.py
│   └── test_catalogue.py
├── app.py                    # Streamlit page composition
├── movie_list.pkl            # 4,800 processed movie tags
├── tmdb_5000_movies.csv      # Local ratings and metadata
├── generate_model.py         # Optional catalogue regeneration utility
├── requirements.txt
└── Dockerfile
```

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests verify the complete catalogue count, title/genre search, stable
movie-ID selection, 20-result recommendations, and TMDB poster/backdrop fallback
behavior without making live network calls.

## Docker

```bash
docker build -t cinematch .
docker run --rm -p 8501:8501 cinematch
```

To enable poster artwork in Docker:

```bash
docker run --rm -p 8501:8501 \
  -e TMDB_BEARER_TOKEN="your_read_access_token" \
  cinematch
```

This product uses the TMDB API but is not endorsed or certified by TMDB.
