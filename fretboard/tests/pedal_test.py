import unittest

from fretboard.pedal import Pedal, E9_PEDAL_CHANGES


class TestPedal(unittest.TestCase):

    def test_get_all_pedal_combinations(self):
        all_combinations: list[list[str]] = Pedal.get_all_pedal_combinations(list(E9_PEDAL_CHANGES.keys()))
        self.assertTrue([] in all_combinations)  # no pedal is a combination
        self.assertTrue(["A"] in all_combinations)
        self.assertTrue(["B"] in all_combinations)
        self.assertTrue(["A", "B"] in all_combinations)
        self.assertTrue(["B", "C"] in all_combinations)
        self.assertTrue(["E"] in all_combinations)
        self.assertTrue(["F"] in all_combinations)
        self.assertTrue(["A", "F"] in all_combinations)
        self.assertTrue(["A", "B", "C"] not in all_combinations)
        self.assertTrue(["D", "G"] not in all_combinations)
        self.assertTrue(["E", "F"] not in all_combinations)
        self.assertTrue(["A/2", "A"] not in all_combinations)
        self.assertTrue(["D/2", "D"] not in all_combinations)


if __name__ == "__main__":
    unittest.main()
