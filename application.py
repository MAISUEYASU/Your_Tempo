from flask import Flask, render_template, request, jsonify
from utils.tempo_calculator import tap
import utils.spotify_client as spotify_client

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

        # Spotifyにプレイリストを作成し、曲を追加
        playlist_id = spotify_client.create_playlist(name=f'Tempo {tempo} Playlist')
        spotify_client.add_tracks_to_playlist(playlist_id, track_ids)

        return jsonify({'message': 'Playlist created successfully!', 'playlist_id': playlist_id})
    return jsonify({'error': 'No tempo provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8888)
