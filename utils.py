import logging
import secrets
import spotipy


def search_tracks_by_tempo(sp, tempo):
    results = sp.current_user_saved_tracks(limit=50)
    matching_tracks = []

    # トラックIDのリストを取得（空でないことを保証）
    track_ids = [
        item['track']['id'] for item in results['items'] if item['track'].get('id')]

    if not track_ids:
        raise ValueError("トラックIDが見つかりません。保存された楽曲を確認してください。")

    try:
        # Spotify APIにリクエスト
        audio_features_list = sp.audio_features(track_ids)
    except spotipy.exceptions.SpotifyException as e:
        # エラーをログに記録
        logging.error(f"Spotify APIエラー: {e}")
        raise

    # テンポに基づいてトラックをフィルタリング
    for i, audio_features in enumerate(audio_features_list):
        if audio_features and abs(audio_features['tempo'] - tempo) < 10:
            matching_tracks.append(results['items'][i]['track'])

    return matching_tracks


def get_tracks_info(tracks):
    return [
        {
            'name': track['name'],
            'artist': ', '.join(
                [artist['name'] for artist in track['artists']]),
            'album_image': track['album']['images'][0]['url'],
            'id': track['id']
        }
        for track in tracks
    ]


def generate_playlist_based_on_bpm(sp, user_id, tracks, playlist_title):
    try:
        # プレイリストの作成
        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_title, public=False
        )

        # トラック ID のリストを取得
        track_ids = [track.get('id') for track in tracks if track.get('id')]

        # トラック ID が取得できなかった場合はエラーを出す
        if not track_ids:
            print("Error: No track URIs found. The track list is empty.")
            raise ValueError("No track URIs found")

        # プレイリストにトラックを追加
        response = sp.user_playlist_add_tracks(
            user=user_id, playlist_id=playlist['id'], tracks=track_ids
        )

        # リクエストの成功を確認
        if response is None:
            print("Error: Failed to add tracks to the playlist.")
            raise ValueError("Failed to add tracks to the playlist")

        return playlist['id'], playlist['external_urls']['spotify']

    except Exception as e:
        # エラーメッセージをログに出力
        print(f"Error in generate_playlist_based_on_bpm: {e}")
        raise


def generate_secret_key():
    """
    秘密鍵を生成するための関数。
    Flaskアプリケーションのセッションに使用。
    """
    return secrets.token_hex(16)
