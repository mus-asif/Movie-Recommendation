import pandas as pd
import streamlit as st
import pickle
import requests

# Replace with your actual OMDB API key
OMDB_API_KEY = '5b14b3fc'

def fetch_poster(movie_title):
    url = f'https://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data:
        return data['Poster']
    else:
        return None

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_title = movies_df.iloc[i[0]].title
        recommended_movies.append(movie_title)
        poster = fetch_poster(movie_title)
        recommended_movies_poster.append(poster)
    return recommended_movies, recommended_movies_poster

# Load the data
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
movies = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(len(recommended_movie_names))
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.write("Poster not available")
