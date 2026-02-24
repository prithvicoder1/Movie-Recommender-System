import pickle
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🍿")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Poster+Not+Available"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.markdown("""
<style>
    /* Main background and fonts */
    .stApp {
        background-color: #141414;
        color: #e5e5e5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Headers and elements */
    h1, h2, h3, p, span, div, label {
        color: #e5e5e5 !important;
    }
    
    /* ===== DROPDOWN FIX: white bg + dark text ===== */
    /* Closed dropdown box */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #2b2b2b !important;
        color: #ffffff !important;
    }

    /* Input text in dropdown */
    .stSelectbox input {
        color: #ffffff !important;
        background-color: #2b2b2b !important;
    }

    /* The floating popup container */
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    /* Each option in the list */
    [data-baseweb="menu"] ul li,
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li *,
    [data-baseweb="option"],
    [data-baseweb="option"] span,
    [data-baseweb="option"] div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Hover highlight */
    [data-baseweb="option"]:hover,
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] li:hover * {
        background-color: #ffe0e0 !important;
        color: #E50914 !important;
    }

    /* Primary Button styling (Netflix Red) */
    .stButton > button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        transition: all 0.2s ease-in-out;
        width: 100%;
        margin-top: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        background-color: #f40612 !important;
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.4);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Movie Image styling & hover */
    img {
        border-radius: 8px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    
    img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.8);
        cursor: pointer;
    }
    
    /* Movie Titles */
    .movie-title {
        font-size: 1.15rem;
        font-weight: 600;
        text-align: center;
        margin-top: 12px;
        color: #ffffff !important;
        text-shadow: 1px 1px 2px black;
    }

    /* Header adjustments */
    .netflix-header {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #E50914 !important;
        text-align: center;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='netflix-header'>Movie Recommender System</h1>", unsafe_allow_html=True)

movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown to get recommendations:",
    movie_list
)

if st.button('Show Recommendation', help="Click to find similar movies"):
    with st.spinner('Finding the best movies for you...'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.image(recommended_movie_posters[0], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[0]}</p>", unsafe_allow_html=True)
        with col2:
            st.image(recommended_movie_posters[1], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[1]}</p>", unsafe_allow_html=True)
        with col3:
            st.image(recommended_movie_posters[2], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[2]}</p>", unsafe_allow_html=True)
        with col4:
            st.image(recommended_movie_posters[3], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[3]}</p>", unsafe_allow_html=True)
        with col5:
            st.image(recommended_movie_posters[4], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{recommended_movie_names[4]}</p>", unsafe_allow_html=True)
