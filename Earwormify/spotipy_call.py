import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

from spotipy.cache_handler import FlaskSessionCacheHandler
from flask import session

#loading in enviorment variables
load_dotenv()

cache_handler = FlaskSessionCacheHandler(session)

client_id = os.getenv("BRANDON_CLIENT_ID")
client_secret = os.getenv("BRANDON_SECRET")

scope = 'user-top-read user-read-private playlist-modify-public user-library-read'

sp_auth = SpotifyOAuth(client_id=client_id , client_secret=client_secret, 
                       redirect_uri='http://localhost:8080/callback', scope=scope, 
                       show_dialog=True, cache_handler=cache_handler)

#creating client object
client = spotipy.Spotify(auth_manager=sp_auth)

#authorizing page url
auth_url = sp_auth.get_authorize_url()



def get_top_artists():

    result = client.current_user_top_artists(limit=20, time_range="medium_term")
    top_artist_list = []
    for item in result['items']:
        top_artist_list.append(item['name'])
    return top_artist_list
    
def get_token():
    return sp_auth.validate_token(cache_handler.get_cached_token())


def create_playlist():
    playlist = client.user_playlist_create(user=client.current_user()["id"], name="earwormify", public=True, description="Earwormify")
    return playlist

def get_all_liked_songs():
    twenty_songs = client.current_user_saved_tracks(limit=50)
    song_list = [track['track']['id'] for track in twenty_songs['items']]
    print(song_list)

    while twenty_songs["next"]: 
        twenty_songs = client.next(twenty_songs)
        song_list.extend([track['track']['id'] for track in twenty_songs['items']])

    return song_list



def sort_songs(sort_method):
    song_ids = get_all_liked_songs()
    song_details = []

    for song_id in song_ids:
        track = client.track(song_id)
        song_details.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'release_date': track['album']['release_date'],
            'genre': track['album']['genres'][0] if 'genres' in track['album'] else 'Unknown'
        })

    if sort_method == 'popularity':
        sorted_songs = sorted(song_details, key=lambda x: x['popularity'], reverse=True)
    elif sort_method == 'release_date':
        sorted_songs = sorted(song_details, key=lambda x: x['release_date'])
    elif sort_method == 'genre':
        sorted_songs = sorted(song_details, key=lambda x: x['genre'])
    else:
        sorted_songs = song_details

    return sorted_songs


