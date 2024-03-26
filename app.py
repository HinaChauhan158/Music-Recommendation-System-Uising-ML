import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import retrying

CLIENT_ID = "3775c6b78f3945feb6dbb20708853551"
CLIENT_SECRET = "6712884a69d9453cb3f0817cf587bc16"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# @retrying.retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the music details
        artist = music.iloc[i[0]].artist
        recommended_music_poster = get_song_album_cover_url(music.iloc[i[0]].song, artist)
        recommended_music_posters.append(recommended_music_poster)
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendations'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with eval(f"col{i+1}"):
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
