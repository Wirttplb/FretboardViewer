import unittest
import json
from pathlib import Path

from fretboard.chord_generator import ChordGenerator
from fretboard.fretboard import Fretboard


class TestChordGenerator(unittest.TestCase):

    def test_open_e_chord_generator(self):
        chords = ChordGenerator.generate_open_e_chords("E")

        # Dump in json
        fretboard = Fretboard.init_as_guitar_open_e()
        path = Path("data/open_e_generated_chords.json")

        with open(path, "w") as file:
            json_dict = {}
            json_dict["chords"] = []
            for chord in chords.values():
                json_dict["chords"].append(chord.to_json(fretboard.tuning))

            json.dump(json_dict, file)

    def test_e9_chord_generator(self):
        chords = ChordGenerator.generate_e9_chords("E")
        self.assertTrue("M" in chords)
        self.assertTrue(chords["M"].voicings[0].pedals == [])
        self.assertTrue("m" in chords)
        self.assertTrue("m7" in chords)
        self.assertTrue("M7" in chords)
        self.assertTrue("sus2" in chords)
        self.assertTrue("sus4" in chords)
        self.assertTrue("add9" in chords)
        self.assertTrue("madd9" in chords)
        self.assertTrue("7" in chords)
        self.assertTrue("M6" in chords)
        self.assertTrue("aug" in chords)
        self.assertTrue("dim" in chords)
        self.assertTrue("Mb5" in chords)
        self.assertTrue("m7b5" in chords)
        self.assertTrue("mb5bb7" in chords)
        self.assertTrue("M6add9" in chords)
        self.assertTrue("M7/6" in chords)
        self.assertTrue("mm6" in chords)
        self.assertTrue("mM6" in chords)
        self.assertTrue("M9" in chords)
        self.assertTrue("9" in chords)
        self.assertTrue("7b9" in chords)
        self.assertTrue("7#9" in chords)
        self.assertTrue("m9" in chords)
        self.assertTrue("mM9" in chords)
        self.assertTrue("b5b13" in chords)
        self.assertTrue("11" in chords)
        self.assertTrue("13" in chords)

        # Dump in json
        fretboard = Fretboard.init_as_pedal_steel_e9()
        path = Path("data/e9_generated_chords.json")

        with open(path, "w") as file:
            json_dict = {}
            json_dict["chords"] = []
            for chord in chords.values():
                json_dict["chords"].append(chord.to_json(fretboard.tuning))

            json.dump(json_dict, file)

        # Test content
        with open(path, "r") as file2:
            data = json.load(file2)

            is_in_json = False
            for chord in data["chords"]:
                if "7#9" == chord["name"]:
                    is_in_json = True
                    break
            self.assertTrue(is_in_json)

            is_in_json = False
            for chord in data["chords"]:
                if "mb5bb7" == chord["name"]:
                    is_in_json = True
                    break
            self.assertTrue(is_in_json)

            is_in_json = False
            for chord in data["chords"]:
                if "M" == chord["name"]:
                    for voicing in chord["voicings"]:
                        if (
                            (voicing["notes"] == [3, "x", 3, "x", 3, 3, 3, 3, "x", "x"])
                            and (voicing["intervals"] == ["1", "x", "3", "x", "5", "1", "3", "5", "x", "x"])
                            and (voicing["pedals"] == ["A", "F"])
                        ):
                            is_in_json = True
                            break
                if is_in_json:
                    break
            self.assertTrue(is_in_json)


if __name__ == "__main__":
    unittest.main()
