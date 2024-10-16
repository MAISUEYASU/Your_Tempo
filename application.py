from flask import Flask, redirect, render_template, request, jsonify, url_for
import cv2
from deepface import DeepFace
from utils.spotify_client import search_tracks_by_tempo, generate_playlist_based_on_bpm, add_tracks_to_playlist, get_tracks_info, sp
from datetime import datetime

app = Flask(__name__, static_folder='static')

# 表情認識
def detect_emotion():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        faces = DeepFace.analyze(frame, actions=['emotion'])
        dominant_emotion = faces['dominant_emotion']
        cap.release()
        return dominant_emotion
    cap.release()
    return "neutral"  # 表情が認識できない場合

# メインページ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # Spotifyの認証URLにリダイレクト
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Spotifyの認証コードを取得
    auth_code = request.args.get('code')
    if auth_code:
        # 認証コードを使用してアクセストークンを取得
        sp.auth_manager.get_access_token(auth_code)
        return redirect(url_for('profile'))  # 認証が成功したらプロファイルページにリダイレクト
    return jsonify({'error': '認証に失敗しました'}), 400

@app.route('/get_user_info')
def get_user_info():
    user_info = sp.current_user()
    if user_info:
        return jsonify({'userName': user_info['display_name']})
    return jsonify({'error': 'ユーザー情報が取得できません'}), 400


@app.route('/profile')
def profile():
    user_info = sp.current_user()
    return render_template('profile.html')

# プレイリスト作成処理
@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    tempo = data.get('tempo')
    
    if tempo:
        # 表情認識を実行
        emotion = detect_emotion()

        #  ユーザーIDを取得
        user_id = sp.current_user()['id']  

        # プレイリストIDとURLを生成
        playlist_id, playlist_url = generate_playlist_based_on_bpm(user_id, tempo)

        # 楽曲情報を取得
        tracks_info = get_tracks_info(search_tracks_by_tempo(tempo))

        return jsonify({
            'message': 'プレイリストの作成に成功しました！',
            'playlist_id': playlist_id,
            'playlist_url': playlist_url, 
            'emotion': emotion, 
            'tracks': tracks_info
        }), 201
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
