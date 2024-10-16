import cv2
from deepface import DeepFace

# カスケード分類器の読み込み（顔検出用）
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ウェブカメラの起動
cap = cv2.VideoCapture(0)

while True:
    # フレームの読み取り
    ret, frame = cap.read()
    # グレースケールに変換（顔検出の精度向上のため）
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 顔を検出
    faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)
    
    for (x, y, w, h) in faces:
        # 顔の部分を切り出す
        face_roi = frame[y:y+h, x:x+w]
        # 顔部分を表示して確認
        cv2.imshow('Face ROI', face_roi)
        try:
            # 表情を認識
            emotion = DeepFace.analyze(face_roi, actions=['emotion'])
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            emotion = {'dominant_emotion': 'N/A'}
        # 表情ラベルを表示
        cv2.putText(frame, emotion['dominant_emotion'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # 映像を表示
    cv2.imshow('Video', frame)
    
    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソース解放
cap.release()
cv2.destroyAllWindows()
