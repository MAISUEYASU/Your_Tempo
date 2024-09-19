from flask import Flask, redirect, render_template, request, jsonify, url_for
from utils.spotify_client import search_tracks_by_tempo, create_playlist, add_tracks_to_playlist, get_tracks_info, sp
from datetime import datetime

app = Flask(__name__, static_folder='static')

# メインページ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/callback')
def callback():
    # Spotifyの認証コードを取得
    auth_code = request.args.get('code')
    
    if auth_code:
        # 認証コードを使用してアクセストークンを取得
        sp.auth_manager.get_access_token(auth_code)
        return redirect(url_for('profile'))  # 認証が成功したらプロファイルページにリダイレクト
    return jsonify({'error': '認証コードがありません'}), 400

@app.route('/profile')
def profile():
    user_info = sp.current_user()
    return f"Hello, {user_info['display_name']}! Welcome to your Spotify profile."

# プレイリスト作成処理
@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.json
    tempo = data.get('tempo')
    
    if tempo:
        # テンポに合った曲を検索
        track_ids = search_tracks_by_tempo(tempo)

        # 現在の日時を取得し、フォーマットする
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S") 

        # 日時を含めたプレイリスト名を作成
        playlist_name = f"Tempo {tempo} Playlist - {formatted_date}"

        # Spotifyにプレイリストを作成し、曲を追加
        playlist_id = create_playlist(name=f'Tempo {tempo} Playlist')
        add_tracks_to_playlist(playlist_id, track_ids)

        # トラック情報（名前とアーティスト）を取得してクライアントに送り返す
        tracks_info = get_tracks_info(track_ids)

        # プレイリストのリンクを生成
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

        return jsonify({
            'message': 'プレイリストの作成に成功したよ！', 
            'playlist_id': playlist_id,
            'tracks': tracks_info  # 曲情報を返す
        })
    return jsonify({'error': 'テンポが指定されていません。'}), 400

@app.route('/calculate-tempo', methods=['POST'])
def calculate_tempo():
    tempo = request.form.get('tempo')  # テンポ値を取得
    # 正しいテンポが取得できていれば結果ページにリダイレクト
    if tempo:
        return redirect(url_for('show_result', tempo=tempo))
    return redirect(url_for('index'))

@app.route('/result')
def show_result():
    tempo = request.args.get('tempo')
    return render_template('/result.html', tempo=tempo)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
