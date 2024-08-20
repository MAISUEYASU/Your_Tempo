from flask import Flask, render_template, request, jsonify
import utils.spotify_client as spotify_client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.json
    tempo = data.get('tempo')
    
    if tempo:
        # Spotify APIを使って曲を検索し、オーディオフィーチャーを取得
        track_ids = spotify_client.search_tracks_by_tempo(tempo)
        tracks_info = spotify_client.get_tracks_info(track_ids)

        return jsonify({'tracks': tracks_info})
    return jsonify({'error': 'No tempo provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8888)
