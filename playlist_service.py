from datetime import datetime

import requests
from utils import (
    search_tracks_by_tempo,
    generate_playlist_based_on_bpm)
from spotify_client import get_spotify_client


def create_playlist(tempo):
    sp = get_spotify_client()
    if not sp or not tempo:
        return {'error': 'Unauthorized or missing tempo'}

    try:
        # ユーザー ID と楽曲を取得
        user_id = sp.current_user()['id']
        tracks = search_tracks_by_tempo(sp, tempo)

        # トラックIDを100件以下に分割
        def split_ids(ids, max_size=100):
            for i in range(0, len(ids), max_size):
                yield ids[i:i + max_size]

        track_batches = list(split_ids(tracks))

        # 各バッチを処理してプレイリスト作成
        playlist_title = f"Tempo{tempo}_{datetime.now().strftime('%Y.%m.%d')}"
        playlist_id, playlist_url = None, None

        for batch in track_batches:
            try:
                # プレイリスト作成を試行
                playlist_id, playlist_url = generate_playlist_based_on_bpm(
                    sp, user_id, batch, playlist_title
                )
            except requests.exceptions.HTTPError as http_err:
                # HTTPエラーの詳細をログ出力
                print(f"HTTPエラーが発生しました: {http_err}")
                print(f"ステータスコード: {http_err.response.status_code}")
                print(f"レスポンス内容: {http_err.response.text}")
                return {'error': 'Failed to create playlist'}
            except Exception as e:
                # その他のエラーをキャッチ
                print(f"予期しないエラーが発生しました: {e}")
                return {'error': 'Server error'}

        return {
            'playlist_url': playlist_url,
            'tracks': tracks
        }
    except Exception as e:
        # 全体的なエラー処理
        print(f"エラー: {e}")
        return {'error': 'Server error'}
