import spotipy 
from spotipy.oauth2 import SpotifyOAuth 
from config.settings import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-private playlist-modify-public"
))

def search_tracks_by_tempo(tempo, limit=10):
    # ターゲットテンポの範囲を設定
    min_tempo = max(0, tempo - 5)
    max_tempo = tempo + 5

    # Spotify APIで楽曲を検索
    results = sp.search(q=f'tempo:{min_tempo}-{max_tempo}', type='track', limit=limit)
    track_ids = [track['id'] for track in results['tracks']['items']]
    return track_ids

def create_playlist(name):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id=user_id, name=name)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_ids):
    sp.playlist_add_items(playlist_id, track_ids)

# ユーザーの好きなアーティストを取得するサンプルコード
def get_favorite_artists(user_id):
    results = sp.current_user_top_artists(limit=10)
    for idx, artist in enumerate(results['items']):
        print(f"{idx + 1}. {artist['name']}")

def get_audio_features(track_ids):
    # Spotify APIからトラックのオーディオフィーチャーを取得
    audio_features = sp.audio_features(track_ids)
    return audio_features

def get_tracks_info(track_ids):
    tracks = sp.tracks(track_ids)['tracks']
    tracks_info = []
    return [{
        'name': track['name'], 
        'artist': track['artists'][0]['name']
        } for track in tracks]
