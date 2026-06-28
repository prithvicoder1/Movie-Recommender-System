<div align="center">

# 🎬 Movie Recommender System

### *Discover your next favorite movie — powered by Machine Learning*

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![TMDB](https://img.shields.io/badge/TMDB-API-01D277?style=for-the-badge&logo=themoviedatabase)](https://www.themoviedb.org/)

</div>

---

## 🚀 Overview

A **content-based movie recommender system** that suggests 5 similar movies for any film you select — complete with beautiful movie posters fetched live from the TMDB API. Built with a Netflix-inspired dark UI and powered by cosine similarity on NLP-processed movie features.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Smart Recommendations** | Suggests 5 movies similar to your selection using cosine similarity |
| 🖼️ **Live Movie Posters** | High-quality posters fetched in real-time from TMDB API |
| 🎨 **Netflix-style UI** | Sleek dark theme with red accents, hover animations & premium design |
| ⚡ **Fast & Responsive** | Pre-computed similarity matrix via pickle for instant results |
| 🔍 **Search & Select** | Type to search or scroll through 4800+ movies |

---

## 🧠 How It Works

The system uses **Content-Based Filtering** — it analyzes the features of each movie and recommends others with the most similar profile.

```
Movie Input
    │
    ▼
Feature Extraction (Genres + Keywords + Cast + Crew + Overview)
    │
    ▼
CountVectorizer (5000 most common words, English stop words removed)
    │
    ▼
Cosine Similarity Matrix (4800 × 4800)
    │
    ▼
Top 5 Most Similar Movies → Fetch Posters from TMDB → Display
```

---

## 📁 Project Structure

```
movie-recommender-system-tmdb-dataset-main/
│
├── app.py                      # Streamlit web application (UI + logic)
├── generate_model.py           # Script to process data & create model files
├── notebook86c26b4f17.ipynb    # Original Jupyter notebook (EDA + model building)
│
├── model/
│   ├── movie_list.pkl          # Processed movie DataFrame
│   └── similarity.pkl          # Pre-computed cosine similarity matrix
│
├── tmdb_5000_movies.csv        # TMDB movies dataset
├── tmdb_5000_credits.csv       # TMDB credits dataset (cast & crew)
│
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/movie-recommender-system-tmdb-dataset.git
cd movie-recommender-system-tmdb-dataset
```

### 2. Install dependencies
```bash
pip install streamlit pandas scikit-learn requests
```

### 3. Download the datasets
Download the TMDB datasets from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and place them in the root directory:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 4. Generate the model files
```bash
python generate_model.py
```
> This creates `model/movie_list.pkl` and `model/similarity.pkl` — only needs to be run once.

### 5. Launch the app
```bash
streamlit run app.py
```

Open your browser and go to **http://localhost:8501** 🎉

---

## 🖥️ App Preview

> Select any movie from the dropdown, click **Show Recommendation**, and get 5 personalized suggestions with movie posters instantly!

---

## 📊 Dataset

| Dataset | Records | Source |
|---|---|---|
| `tmdb_5000_movies.csv` | 4,803 movies | [TMDB on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) |
| `tmdb_5000_credits.csv` | 4,803 records | [TMDB on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) |

**Features used for similarity:**
- 📝 Movie overview (plot summary)
- 🎭 Genres
- 🔑 Keywords
- 🎬 Top 3 cast members
- 🎥 Director

---

## 🛠️ Tech Stack

- **[Python 3.7+](https://www.python.org/)** — Core language
- **[Streamlit](https://streamlit.io/)** — Web app framework
- **[Pandas](https://pandas.pydata.org/)** — Data processing
- **[scikit-learn](https://scikit-learn.org/)** — `CountVectorizer` & `cosine_similarity`
- **[TMDB API](https://www.themoviedb.org/documentation/api)** — Movie poster images
- **Pickle** — Model serialization for fast load times

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

<div align="center">

Made with ❤️ using Python & Streamlit

⭐ **Star this repo if you found it helpful!** ⭐

</div>
