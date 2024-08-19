def calculate_tempo(tap_times):
    intervals = [j-i for i, j in zip(tap_times[:-1], tap_times[1:])]
    tempo = 60.0 / (sum(intervals) / len(intervals))
    return tempo
