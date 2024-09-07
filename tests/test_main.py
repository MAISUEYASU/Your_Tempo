from utils.tempo_calculator import calculate_tempo
import unittest

class TestTempoCalculator(unittest.TestCase):
    def test_calculate_tempo(self):
        tap_times = [0, 1, 2]  # 秒単位のタップ時間
        tempo = calculate_tempo(tap_times)
        expected_tempo = 60.0  # 1秒間隔なら60BPM
        self.assertAlmostEqual(tempo, expected_tempo)

if __name__ == "__main__":
    unittest.main()
