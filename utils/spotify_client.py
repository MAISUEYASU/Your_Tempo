import spotipy 
from spotipy.oauth2 import SpotifyOAuth 
from config.settings import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-private playlist-modify-public user-library-read"
))

def ensure_token_valid():
    # トークンの有効性を確認し、リフレッシュが必要であればリフレッシュ
    token_info = sp.auth_manager.get_access_token(as_dict=True)
    # print(token_info) # デバッグ用: token_infoの内容を確認

    if sp.auth_manager.is_token_expired(token_info):
        print("Token expired, refreshing...")
        sp.auth_manager.refresh_access_token(token_info['refresh_token'])
    else:
        print("Token is valid")

def search_tracks_by_tempo(tempo, limit=10):
    ensure_token_valid()  # トークンの有効性を確認してリフレッシュ
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

    # プレイリストのURLを生成して返す
    playlist_url = f"https://open.spotify.com/playlist/{playlist['id']}"
    return playlist['id'], playlist_url  # プレイリストIDとURLを返す

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
    track_info_list = []

    for track in tracks:
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        track_info_list.append({
            'name': track['name'], 
            'artist': artist_names,  
            'album_image': track['album']['images'][0]['url'] if track['album']['images'] else '',
            'id': track['id']  # トラックIDを追加して返す
        })

    return track_info_list
