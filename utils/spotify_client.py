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

def generate_playlist_based_on_bpm(user_id, tempo, limit=10):
    # 現在の日時を取得してプレイリスト名を作成
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    playlist_name = f"Tempo {tempo} - {now}"

    # プレイリストを作成
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)

    # テンポに合った曲を検索し、プレイリストに追加
    track_ids = search_tracks_by_tempo(tempo, limit=limit)
    sp.playlist_add_items(playlist['id'], track_ids)

    # プレイリストIDを返す
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_ids):
    sp.playlist_add_items(playlist_id, track_ids)

# ユーザーの好きなアーティストを取得するサンプルコード
def get_favorite_artists(user_id):
    results = sp.current_user_top_artists(limit=10)
    for idx, artist in enumerate(results['items']):
        print(f"{idx + 1}. {artist['name']}")

# Spotify APIからトラックのオーディオフィーチャーを取得
def get_audio_features(track_ids):
    audio_features = sp.audio_features(track_ids)
    return audio_features

def get_tracks_info(track_ids):
    tracks = sp.tracks(track_ids)['tracks']
    return [{
        'name': track['name'], 
        'artist': track['artists'][0]['name'],
        'album_image': track['album']['images'][0]['url']  # ジャケット画像のURL
    } for track in tracks]