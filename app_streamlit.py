import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import songrecommendations
import polarplot

SPOTIPY_CLIENT_ID = 'e18fafeb60a949d2a9b7d1efccabe69a'
SPOTIPY_CLIENT_SECRET = '739bbbed49864382a64a64ccd64ecdcc'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.header('Rockstar Spotify App (Streamlit)')

search_choices = ['Song/Track', 'Artist', 'Album']
search_selected = st.sidebar.selectbox("Your search choice please: ", search_choices)

search_keyword = st.text_input(search_selected + " (Keyword Search)")
button_clicked = st.button("Search")

search_results = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    if search_selected == 'Song/Track':
        st.write("Start song/track search")
        tracks = sp.search(q='track:' + search_keyword, type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        for track in tracks_list:
            search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])

    elif search_selected == 'Artist':
        st.write("Start artist search")
        artists = sp.search(q='artist:' + search_keyword, type='artist', limit=20)
        artists_list = artists['artists']['items']
        for artist in artists_list:
            search_results.append(artist['name'])

    elif search_selected == 'Album':
        st.write("Start album search")
        albums = sp.search(q='album:' + search_keyword, type='album', limit=20)
        albums_list = albums['albums']['items']
        for album in albums_list:
            search_results.append(album['name'] + " - By - " + album['artists'][0]['name'])

selected_album = None
selected_artist = None
selected_track = None

if search_selected == 'Song/Track':
    selected_track = st.selectbox("Select your song/track: ", search_results)
elif search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist: ", search_results)
elif search_selected == 'Album':
    selected_album = st.selectbox("Select your album: ", search_results)

if selected_track is not None and len(tracks_list) > 0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                if 'images' in track['album'] and len(track['album']['images']) > 1:
                    img_album = track['album']['images'][1]['url']
                    songrecommendations.save_album_image(img_album, track_id)
                break

    if track_id is not None:
        image = songrecommendations.get_album_image(track_id)  # Corrected function name
        if image is not None:
            st.image(image)
            track_choices = ['Song Features', 'Similar Songs Recommendation']
            selected_track_choice = st.sidebar.selectbox('Please select track choice: ', track_choices)
            if selected_track_choice == 'Song Features':
                track_features = sp.audio_features(track_id)
                df = pd.DataFrame(track_features, index=[0])
                df_features = df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                st.dataframe(df_features)
                polarplot.feature_plot(df_features)
            elif selected_track_choice == 'Similar Songs Recommendation':
                token = songrecommendations.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                similar_songs_json = songrecommendations.get_track_recommendations(track_id, token)
                recommendation_list = similar_songs_json['tracks']
                recommendation_df = pd.DataFrame(recommendation_list)[['name', 'explicit', 'duration_ms', 'popularity']]
                st.dataframe(recommendation_df)
                songrecommendations.song_recommendation_vis(recommendation_df)
        else:
            st.write("Failed to retrieve album image.")

    else:
        st.write("Please select a track from the list")

# Add similar logic for albums and artists selections

