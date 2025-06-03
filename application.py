from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
    session
)
import logging

import requests
from spotify_client import (
    get_spotify_client,
    sp_oauth,
    save_token
)
from utils import generate_playlist_based_on_bpm, generate_secret_key, search_tracks_by_tempo

app = Flask(__name__, static_folder='static')

# セッション用の秘密鍵を設定
app.secret_key = generate_secret_key()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/countTempo')
def count_tempo():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    user_info = sp.current_user()
    username = user_info.get('display_name', 'User')
    return render_template('countTempo.html', username=username)


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        save_token(token_info)
        return redirect(url_for('count_tempo'))
    except Exception as e:
        logging.error(f"Callback error: {e}")
        return jsonify({'error': 'Failed to authenticate with Spotify'}), 500


@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    tempo = request.json.get('tempo')
    logging.info(f"プレイリスト作成リクエストを受信しました: テンポ {tempo}")
    try:
        sp = get_spotify_client()
        if not sp:
            logging.error("Spotifyクライアントを取得できません。トークンが無効または期限切れです。")
            return jsonify({'error': 'Unauthorized: Missing or expired token'}), 401

        user_id = sp.current_user()['id']
        tracks = search_tracks_by_tempo(sp, tempo)

        if not tracks:
            return jsonify({'error': '楽曲が見つかりませんでした。'}), 400

        playlist_id, playlist_url = generate_playlist_based_on_bpm(
            sp, user_id, tracks, f"Playlist for Tempo {tempo}"
        )
        return jsonify({'playlist_url': playlist_url}), 201
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logging.error(f"403エラー詳細: {e.response.text}")
        return jsonify({'error': 'Failed to create playlist'}), 500
    except Exception as e:
        logging.error(f"プレイリスト作成中に予期しないエラーが発生しました: {e}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        sp = get_spotify_client()
        if not sp:
            logging.error("Spotify クライアントを初期化できませんでした: トークンが見つからないか期限切れです。")
            return jsonify({
                'error': 'Unauthorized: Missing or expired token'
                }), 401

        user_info = sp.current_user()
        return jsonify({'userName': user_info.get('display_name', 'Unknown')})
    except Exception as e:
        logging.error(f"Unexpected error in /get_user_info: {e}")
        return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8888)
