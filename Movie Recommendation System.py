import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load data
movies = pd.read_csv('https://raw.githubusercontent.com/satishgunjal/datasets/main/tmdb_5000_movies.csv')

# Fill missing values
movies['overview'] = movies['overview'].fillna('')

# TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'])

# Cosine similarity
similarity = cosine_similarity(tfidf_matrix)

# Function to recommend movies
def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# Streamlit UI
st.title("🎥 Movie Recommender")
movie_input = st.selectbox("Select a Movie:", movies['title'].head(1000))

if st.button("Recommend"):
    recommendations = recommend(movie_input)
    st.write("Top 5 Recommendations:")
    for m in recommendations:
        st.write(f"- {m}")
