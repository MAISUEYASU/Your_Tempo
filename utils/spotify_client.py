import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read"
))

def get_audio_features(track_ids):
    return sp.audio_features(track_ids)
