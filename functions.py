import spotipy
import numpy as np
import pandas as pd
from time import sleep
from tqdm.notebook import tqdm
from spotipy.oauth2 import SpotifyClientCredentials
from config import *

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


# Create a function to search a given single song in the Spotify API
def search_song(artist_name, track_title):
    search_query = f"artist:{artist_name} track:{track_title}"
    results = sp.search(q=search_query, type='track', limit=10)
    track_names_list = []
    artist_list = []
    album_name_list = []
    if results['tracks']['items']:
        for track in results['tracks']['items']:
            track_name = track['name']
            artists = ", ".join([artist['name'] for artist in track['artists']])
            album_name = track['album']['name']
            track_uri = track['uri']
            track_id = track['id']
            track_href = track['href']
            print(f"Track Name: {track_name}\nArtists: {artists}\nAlbum: {album_name}")
            #append to list
            track_names_list.append(track_name)
            artist_list.append(artists)
            album_name_list.append(album_name)
    else:
        print(f"No results found for '{track_title}' by '{artist_name}'.")
    results_df = pd.DataFrame({"Title": track_names_list, "Artist": artist_list, "Album": album_name_list})
    return results_df

# Create function to search for the ID's of a list of songs
def songs_ids(df):
    id_song = []
    
    pbar_1 = tqdm(len(df))
    pbar_2 = tqdm(2)
    for i in range(0, len(df), 2):
        chunk = df.iloc[i:i+2]

        for index, row in chunk.iterrows():
            title = row["Title"]
            artist = row["Artist"]
            query = " track: " + title + "artist: " + artist        

            try:
                results = sp.search(q=query, limit=1)
                song_id = results["tracks"]["items"][0]["id"]
                id_song.append(song_id)
            except:
                song_id = np.nan
                id_song.append(song_id)
                print(f"ID not found for {row['Title']} by {row['Artist']}")
            pbar_2.update(n=1)
        pbar_2.update(0)
        pbar_1.update(n=1)
        sleep(2)

    df['ids'] = id_song

    return df


def add_audio_features(df, audio_features_df):
    df_features = pd.concat([df, audio_features_df], axis=1)
    return df_features

# Create function to obtain the audio features of a given list of songs
def get_audio_features(list_of_songs_ids):
    df = pd.DataFrame()

    for song_id in list_of_songs_ids:
        my_dict = sp.audio_features(song_id)[0]
        my_dict_new = { key:[my_dict[key]] for key in list(my_dict.keys()) }
        df = pd.concat([df, pd.DataFrame(my_dict_new)], axis=0)

    return df