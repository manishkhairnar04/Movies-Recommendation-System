import pickle 
import streamlit as st
import requests
import pandas

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_path = fetch_poster(movie_id)
        if poster_path:
            recommended_movies_poster.append(poster_path)
            recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.header("Movies Recommendation System using Machine Learning")

# Load the movie list and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similary.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    if len(recommended_movies_name) == 0 or len(recommended_movies_poster) == 0:
        st.write("No recommendations available.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movies_name[0])
            st.image(recommended_movies_poster[0])
        with col2:
            st.text(recommended_movies_name[1])
            st.image(recommended_movies_poster[1])
        with col3:
            st.text(recommended_movies_name[2])
            st.image(recommended_movies_poster[2])
        with col4:
            st.text(recommended_movies_name[3])
            st.image(recommended_movies_poster[3])
        with col5:
            st.text(recommended_movies_name[4])
            st.image(recommended_movies_poster[4])
