import time

# タップの時間を記録するリスト
tap_times = []

# タップごとに呼び出される関数
def tap():
    current_time = time.time()
    tap_times.append(current_time)
    
    # 少なくとも2回のタップが必要
    if len(tap_times) > 1:
        bpm = calculate_tempo(tap_times)
    print(f"BPM: {bpm}")


# BPM（テンポ）を計算する関数
def calculate_tempo(tap_times):
    if len(tap_times) < 2:
        print("タップ回数が足りません")
        return None
    
    # 各タップの時間間隔を計算
    intervals = [tap_times[i] - tap_times[i - 1] for i in range(1, len(tap_times))]
    average_interval = sum(intervals) / len(intervals)
    
    # BPMに変換（60秒を割ることで1分あたりのビート数になる）
    bpm = 60 / average_interval
    return bpm





