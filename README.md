<div align="center">

# 🍿 Movie Recommender System

### Discover your next favourite movie — instantly.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![TMDB](https://img.shields.io/badge/TMDB_API-01D277?style=for-the-badge&logo=themoviedatabase&logoColor=white)](https://www.themoviedb.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/prithvicoder1/Movie-Recommender-System?style=for-the-badge&color=yellow)](https://github.com/prithvicoder1/Movie-Recommender-System/stargazers)

<br/>

> A content-based movie recommendation engine that suggests 5 similar movies based on your selection, complete with live posters fetched from the TMDB API — all wrapped in a sleek Netflix-inspired UI.

<br/>

![Demo Banner](assets/demo.png)

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎬 About the Project

**Movie Recommender System** is a machine learning web app that takes a movie you love and instantly recommends 5 similar titles — each displayed with its official poster fetched live from The Movie Database (TMDB) API.

The engine is built on **content-based filtering** using cosine similarity across movie metadata (genres, cast, crew, keywords, and overview). No user history or login required — just pick a movie and go.

---

## ✨ Features

- 🔍 **Smart search** — type or select any movie from 5,000+ titles
- 🎯 **Content-based recommendations** — powered by cosine similarity on TF-IDF vectors
- 🖼️ **Live posters** — real-time poster fetching via the TMDB API
- 🎨 **Netflix-inspired UI** — dark theme, red accents, hover animations
- ⚡ **Fast inference** — pre-computed similarity matrix loaded from `.pkl` for instant results
- 📦 **Dockerized** — ready to containerise and deploy anywhere

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.10+ |
| **Web App** | Streamlit |
| **ML / NLP** | scikit-learn, pandas, NumPy |
| **Similarity** | Cosine Similarity on Count Vectors |
| **Poster API** | TMDB REST API |
| **Model Storage** | Pickle (`.pkl`) |
| **Containerisation** | Docker |
| **Version Control** | Git, GitHub |

---

## 🧠 How It Works

```
User selects a movie
        │
        ▼
 Look up movie index in DataFrame
        │
        ▼
 Retrieve pre-computed cosine similarity row
        │
        ▼
 Sort all movies by similarity score (descending)
        │
        ▼
 Pick top 5 results (excluding the selected movie)
        │
        ▼
 Fetch poster for each via TMDB API
        │
        ▼
 Display titles + posters in a 5-column Streamlit layout
```

The similarity matrix is built from a **Bag of Words** representation of combined movie tags (overview + genres + keywords + cast + director), vectorised with `CountVectorizer` and measured with **cosine similarity**.

---

## 📂 Project Structure

```
Movie-Recommender-System/
│
├── 📁 model/
│   └── movie_list.pkl          # Preprocessed movie DataFrame
│
├── 📁 templates/               # HTML templates (if any)
├── 📁 myenv/                   # Virtual environment (excluded from git)
│
├── 🐍 app.py                   # Main Streamlit application
├── 🐍 generate_model.py        # Script to build similarity matrix
├── 📦 similarity.pkl           # Pre-computed cosine similarity matrix
├── 📦 movie_list.pkl           # Movie metadata
├── 📋 requirements.txt         # Python dependencies
├── 🐳 Dockerfile               # Docker configuration
├── ⚙️  setup.sh                # Setup script
├── 📓 notebook86c26b4f...      # Jupyter EDA notebook
└── 📄 README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- A free [TMDB API key](https://www.themoviedb.org/settings/api)

### 1. Clone the repository

```bash
git clone https://github.com/prithvicoder1/Movie-Recommender-System.git
cd Movie-Recommender-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
source myenv/bin/activate        # Windows: myenv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your TMDB API key

Open `app.py` and replace the API key in `fetch_poster()`:

```python
url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
```

### 5. Generate the model (if `.pkl` files are missing)

```bash
python generate_model.py
```

### 6. Run the app

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

### 🐳 Docker (optional)

```bash
docker build -t movie-recommender .
docker run -p 8501:8501 movie-recommender
```

---

## 📸 Screenshots

| Home Screen | Recommendations |
|---|---|
| ![Home](assets/home.png) | ![Results](assets/results.png) |

> *Add screenshots to an `assets/` folder in your repo to display them here.*

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ❤️ by [Prithvi](https://github.com/prithvicoder1)

⭐ If you found this useful, give it a star — it helps a lot!

</div>
