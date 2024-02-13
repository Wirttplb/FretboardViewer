from __future__ import annotations
from typing import Optional, Any
from copy import copy


class Fretboard:
    """Class representing a fretboard"""

    tuning: list[int]  # notes are represented as integers from 0 to 11

    def __init__(self, tuning: list[int]):
        self.tuning = tuning

    @staticmethod
    def init_from_tuning(tuning: list[str]) -> Fretboard:
        fretboard = Fretboard(convert_str_notes_to_int(tuning))
        return fretboard

    @staticmethod
    def init_as_guitar_standard() -> Fretboard:
        return Fretboard.init_from_tuning(["E", "A", "D", "G", "G", "E"])

    @staticmethod
    def init_as_guitar_open_e() -> Fretboard:
        return Fretboard.init_from_tuning(["E", "B", "E", "G#", "B", "E"])

    @staticmethod
    def init_as_pedal_steel_e9() -> Fretboard:
        return Fretboard.init_from_tuning(["B", "D", "E", "F#", "G#", "B", "E", "G#", "D#", "F#"])

    def get_tuning_as_str(self, as_sharps: bool = True) -> list[str]:
        return convert_int_notes_to_str(self.tuning, as_sharps)

    def generate_fretboard(self, start_fret: int, end_fret: int) -> list[list[int]]:
        """Generate notes for the fretboard between given frets"""
        all_notes = []

        for open_string_note in self.tuning:
            string_notes = []
            for fret in range(start_fret, end_fret + 1):
                string_notes.append((open_string_note + fret) % 12)

            all_notes.append(string_notes)

        return all_notes

    def generate_major_scale_as_integers(self, key: str, start_fret: int, end_fret: int) -> list[list[Optional[int]]]:
        """Generate major scale notes for given key"""
        key_as_int = convert_str_note_to_int(key)
        fretboard = self.generate_fretboard(start_fret, end_fret)
        intervals = [0, 2, 4, 5, 7, 9, 11]

        fretboard_scale = []
        for string_notes in fretboard:
            string_scale = []
            for note in string_notes:
                interval = (note - key_as_int) % 12
                string_scale.append(note if interval in intervals else None)

            fretboard_scale.append(string_scale)

        return fretboard_scale

    def generate_major_scale_as_intervals(self, key: str, start_fret: int, end_fret: int) -> list[list[Optional[str]]]:
        fretboard_scale: list[Any] = self.generate_major_scale_as_integers(key, start_fret, end_fret)

        return self.convert_fretboard_scale_to_intervals(key, fretboard_scale)

    @staticmethod
    def convert_fretboard_scale_to_intervals(key: str, fretboard_scale: list[list[Optional[int]]]) -> list[list[Optional[str]]]:
        fretboard_scale_as_intervals: list[Any] = copy(fretboard_scale)
        key_as_int = convert_str_note_to_int(key)

        for string_scale in fretboard_scale_as_intervals:
            for i_fret, note in enumerate(string_scale):
                if note is not None:
                    interval = (note - key_as_int) % 12 + 1
                    string_scale[i_fret] = convert_int_interval_to_str(interval)

        return fretboard_scale_as_intervals


def convert_str_notes_to_int(notes: list[str]) -> list[int]:
    return [convert_str_note_to_int(note) for note in notes]


def convert_int_notes_to_str(notes: list[int], as_sharps: bool = False) -> list[str]:
    return [convert_int_note_to_str(note, as_sharps) for note in notes]


def convert_str_note_to_int(note: str) -> int:
    if note == "C":
        return 0
    elif note == "C#" or note == "Db":
        return 1
    elif note == "D":
        return 2
    elif note == "D#" or note == "Eb":
        return 3
    elif note == "E":
        return 4
    elif note == "F":
        return 5
    elif note == "F#" or note == "Gb":
        return 6
    elif note == "G":
        return 7
    elif note == "G#" or note == "Ab":
        return 8
    elif note == "A":
        return 9
    elif note == "A#" or note == "Bb":
        return 10
    elif note == "B":
        return 11

    raise ValueError("Invalid note!")


def convert_int_note_to_str(note: int, as_sharps: bool = False) -> str:
    if note == 0:
        return "C"
    elif note == 1:
        return "Db" if not as_sharps else "C#"
    elif note == 2:
        return "D"
    elif note == 3:
        return "Eb" if not as_sharps else "D#"
    elif note == 4:
        return "E"
    elif note == 5:
        return "F"
    elif note == 6:
        return "Gb" if not as_sharps else "F#"
    elif note == 7:
        return "G"
    elif note == 8:
        return "Ab" if not as_sharps else "G#"
    elif note == 9:
        return "A"
    elif note == 10:
        return "Bb" if not as_sharps else "A#"
    elif note == 11:
        return "B"

    raise ValueError("Invalid note!")


def convert_int_interval_to_str(note: int) -> str:
    if note == 1:
        return "1"
    elif note == 2:
        return "b2"
    elif note == 3:
        return "2"
    elif note == 4:
        return "b3"
    elif note == 5:
        return "3"
    elif note == 6:
        return "4"
    elif note == 7:
        return "b5"
    elif note == 8:
        return "5"
    elif note == 9:
        return "b6"
    elif note == 10:
        return "6"
    elif note == 11:
        return "b7"
    elif note == 12:
        return "7"

    raise ValueError("Invalid interval!")