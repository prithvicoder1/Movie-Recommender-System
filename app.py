import streamlit as st
import pickle
import requests
from pathlib import Path

# Page config for better appearance
st.set_page_config(
    page_title="MovieMatch - Your Personal Cinema Guide",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Netflix-style UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Global Styles */
    .stApp {
        background-color: #0c0c0c;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Main Container */
    .main-container {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Header Styling */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 4rem !important;
        text-align: center;
        background: linear-gradient(90deg, #e50914, #b20710);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        text-align: center;
        color: #a3a3a3;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* Dropdown/Selectbox Styling */
    div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: white !important;
    }

    /* Recommendation Button */
    .stButton > button {
        background: linear-gradient(90deg, #e50914, #b20710) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5);
    }

    /* Movie Card Styling */
    .movie-card {
        background-color: #1a1a1a;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid #222;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .movie-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: #e50914;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .movie-poster-container {
        position: relative;
        width: 100%;
        padding-top: 150%; /* 2:3 aspect ratio */
    }

    .movie-poster {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .movie-info {
        padding: 1rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .movie-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .movie-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
    }

    .movie-rating {
        background-color: rgba(229, 9, 20, 0.2);
        color: #ff3333;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Recommendations Grid Spacing */
    .recommendation-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 2rem;
        padding: 1rem 0;
    }
    
    .movie-card-wrapper {
        max-width: 200px;
        margin: 0 auto;
    }

    /* Selected Movie Feature Section */
    .selected-movie-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #0c0c0c 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 3rem;
        border: 1px solid #333;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0c0c0c;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #e50914;
    }
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f"https://api.tmdb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        st.warning(f"Error fetching poster for {movie_id}")
    
    # Fallback image
    return "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

def recommend(movie_name, movies_df, similarity_matrix):
    try:
        index = movies_df[movies_df['title'] == movie_name].index[0]
        distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
        
        recommendations = []
        for i in distances[1:5]: # Get top 4 recommendations
            movie_id = movies_df.iloc[i[0]].movie_id
            recommendations.append({
                'title': movies_df.iloc[i[0]].title,
                'poster': fetch_poster(movie_id),
                'overview': movies_df.iloc[i[0]].overview,
                'rating': movies_df.iloc[i[0]].vote_average
            })
        return recommendations
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

# Load data
base_dir = Path(__file__).resolve().parent
model_dir = base_dir / "model"
movie_list_path = model_dir / "movie_list.pkl"
similarity_path = model_dir / "similarity.pkl"

@st.cache_resource
def load_models():
    if movie_list_path.exists() and similarity_path.exists():
        with open(movie_list_path, 'rb') as f:
            movies_df = pickle.load(f)
        with open(similarity_path, 'rb') as f:
            similarity_matrix = pickle.load(f)
        return movies_df, similarity_matrix
    return None, None

movies_df, similarity_matrix = load_models()

if movies_df is None:
    st.error("Model files not found. Please run the data processing script.")
    st.stop()

# Layout
st.markdown("<h1 class='hero-title'>MOVIE MATCH</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Discover your next cinematic obsession with AI-powered recommendations</p>", unsafe_allow_html=True)

col_mid = st.columns([1, 2, 1])
with col_mid[1]:
    selected_movie = st.selectbox(
        "Search or choose a movie",
        movies_df['title'].values,
        index=0
    )
    
    show_rec = st.button('GENERATE RECOMMENDATIONS')

if show_rec:
    # First, show details about the selected movie
    selected_movie_data = movies_df[movies_df['title'] == selected_movie].iloc[0]
    movie_id = selected_movie_data.movie_id
    
    st.markdown("---")
    
    # Hero section for selected movie
    hero_col1, hero_col2 = st.columns([1, 2.5])
    
    with hero_col1:
        poster_url = fetch_poster(movie_id)
        st.markdown(f"""
        <div class="movie-card-wrapper">
            <div style="position: relative; width: 100%; padding-top: 150%; border-radius: 12px; overflow: hidden; border: 1px solid #222; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <img src="{poster_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;">
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with hero_col2:
        st.title(selected_movie)
        st.subheader(f"⭐ TMDB Rating: {selected_movie_data.vote_average}/10")
        st.write("### Overview")
        st.write(selected_movie_data.overview)
    
    st.markdown("---")
    st.markdown("### 🎬 Because you liked this...")
    
    with st.spinner('Curating recommendations...'):
        recommendations = recommend(selected_movie, movies_df, similarity_matrix)
        
        if recommendations:
            # Display recommendations in a cleaner 4-column grid
            # This makes the images smaller and the layout neater
            cols_per_row = 4
            for i in range(0, len(recommendations), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(recommendations):
                        movie = recommendations[idx]
                        with cols[j]:
                            st.markdown(f"""
                            <div class="movie-card-wrapper">
                                <div class="movie-card">
                                    <div class="movie-poster-container">
                                        <img src="{movie['poster']}" class="movie-poster">
                                    </div>
                                    <div class="movie-info">
                                        <div class="movie-title">{movie['title']}</div>
                                        <div class="movie-meta">
                                            <span class="movie-rating">⭐ {movie['rating']:.1f}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found.")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 0.8rem;'>Powered by TMDB API & Streamlit • Made with ❤️ for Movie Buffs</p>", unsafe_allow_html=True)
