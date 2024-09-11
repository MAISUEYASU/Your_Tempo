from flask import Flask, redirect, render_template, request, jsonify, url_for
from utils.tempo_calculator import tap
import utils.spotify_client as spotify_client
from datetime import datetime

app = Flask(__name__)

# メインページ
@app.route('/')
def index():
    return render_template('index.html')

# プレイリスト作成処理
@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.json
    tempo = data.get('tempo')
    
    if tempo:
        # テンポに合った曲を検索
        track_ids = spotify_client.search_tracks_by_tempo(tempo)

        # 現在の日時を取得し、フォーマットする
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S") 

        # 日時を含めたプレイリスト名を作成
        playlist_name = f"Tempo {tempo} Playlist - {formatted_date}"

        # Spotifyにプレイリストを作成し、曲を追加
        playlist_id = spotify_client.create_playlist(name=f'Tempo {tempo} Playlist')
        spotify_client.add_tracks_to_playlist(playlist_id, track_ids)

        # プレイリストのリンクを生成
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

        return jsonify({'message': 'Playlist created successfully!', 'playlist_id': playlist_id})
    return jsonify({'error': 'No tempo provided'}), 400

@app.route('/calculate-tempo', methods=['POST'])
def calculate_tempo():
    tempo = request.form['tempo']  # テンポ値を取得
    # 正しいテンポが取得できていれば結果ページにリダイレクト
    if tempo:
        return redirect(url_for('show_result', tempo=tempo))
    return redirect(url_for('index'))

@app.route('/result')
def show_result():
    tempo = request.args.get('tempo', None)
    return render_template('/result.html', tempo=tempo)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
