import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read"
))

def search_tracks_by_tempo(tempo, limit=10):
    # ターゲットテンポの範囲を設定
    min_tempo = max(0, tempo - 5)
    max_tempo = tempo + 5

    # Spotify APIで楽曲を検索
    results = sp.search(q=f'tempo:{min_tempo}-{max_tempo}', type='track', limit=limit)
    track_ids = [track['id'] for track in results['tracks']['items']]
    return track_ids

def get_tracks_info(track_ids):
    tracks = sp.tracks(track_ids)['tracks']
    tracks_info = []
    for track in tracks:
        tracks_info.append({
            'name': track['name'],
            'artist': track['artists'][0]['name']
        })
    return tracks_info
