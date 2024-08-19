import unittest
from utils.tempo_calculator import calculate_tempo

class TestTempoCalculator(unittest.TestCase):
    def test_calculate_tempo(self):
        tap_times = [0, 1, 2]
        tempo = calculate_tempo(tap_times)
        self.assertAlmostEqual(tempo, 60.0)

if __name__ == '__main__':
    unittest.main()
