import json
import spotipy
import logging
from flask import session
from spotipy.oauth2 import SpotifyOAuth
from settings import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SCOPE
)

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
)


# トークンをセッションに保存
def save_token(token_info):
    session['token_info'] = token_info


# セッションからトークンをロード
def load_token():
    return session.get('token_info')


# Spotifyクライアントの初期化
def get_spotify_client():
    try:
        # トークンをロード
        token_info = load_token()
        if not token_info:
            logging.error("トークンが見つかりません。ユーザーは再認証する必要があります。")
            return None

        # トークンの有効期限を確認
        if sp_oauth.is_token_expired(token_info):
            logging.info("アクセス トークンの有効期限が切れています。トークンを更新中...")
            try:
                token_info = sp_oauth.refresh_access_token(
                    token_info['refresh_token'])
                save_token(token_info)
                logging.info("アクセス トークンが正常に更新されました。")
            except Exception as e:
                logging.error(f"トークンの更新に失敗しました: {e}")
                return None

        # Spotifyクライアントを返す
        logging.info("Spotify クライアントが正常に初期化されました。")
        return spotipy.Spotify(auth=token_info['access_token'])

    except Exception as e:
        logging.error(f"get_spotify_client で予期しないエラーが発生しました: {e}")
        return None
