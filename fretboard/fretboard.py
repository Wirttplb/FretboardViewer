from __future__ import annotations
from typing import Optional, Any
from copy import copy

from fretboard.chords import Voicing
from fretboard.pedal import Pedal, E9_PEDAL_CHANGES
from fretboard.notes_utils import convert_str_note_to_int, convert_str_notes_to_int, convert_int_notes_to_str, convert_int_interval_to_str


class Fretboard:
    """Class representing a fretboard"""

    tuning: list[int] = []  # notes are represented as integers from 0 to 11
    pedals: list[Pedal] = []  # pedals (or levers)

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
        fretboard = Fretboard.init_from_tuning(["B", "D", "E", "F#", "G#", "B", "E", "G#", "D#", "F#"])
        for pedal in E9_PEDAL_CHANGES.keys():
            fretboard.pedals.append(Pedal.init_from_name(pedal))

        return fretboard

    def get_tuning_as_str(self, as_sharps: bool = True) -> list[str]:
        return convert_int_notes_to_str(self.tuning, as_sharps)

    def get_pedals_as_str(self) -> list[str]:
        return [pedal.name for pedal in self.pedals]

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
        """Generate major scale notes for given key ; a fretboard scale contains a string scale for each string (Optional ints)"""
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

    def generate_voicing(self, voicing: Voicing) -> list[list[Optional[int]]]:
        base_key_as_int = convert_str_note_to_int("C")
        fretboard_scale: list[list[Optional[int]]] = []
        fretboard = self.generate_fretboard(0, 12)

        if len(fretboard) != len(voicing.notes):
            raise ValueError("Voicing and tuning do not match!")

        for string_i, string_notes in enumerate(fretboard):  # loop on all strings
            string_scale = []
            voicing_fret = voicing.notes[string_i]

            for string_note in string_notes:  # loop on all frets
                string_scale.append(None)

                if voicing_fret != None:
                    voicing_note = (voicing_fret + self.tuning[string_i]) % 12

                    if voicing_note == string_note:
                        voicing_note_in_key = (voicing_note - base_key_as_int) % 12  # output with respect to C
                        string_scale[-1] = voicing_note_in_key

            fretboard_scale.append(string_scale)

        return fretboard_scale

    def get_all_pedal_combinations(self) -> list[list[str]]:
        return Pedal.get_all_pedal_combinations([pedal.name for pedal in self.pedals])

    def get_intervals_at_fret(self, fret: int, pedals: list[Pedal], key: str = "E") -> list[int]:
        """Get notes as interval (as int) at given fret with given pedals applied

        Args:
            fret (int): fret number
            pedals (list[Pedal]): pedals to apply

        Returns:
            list[int]: notes at fret
        """
        key_as_int = convert_str_note_to_int(key)
        pedals_as_str = self.get_pedals_as_str()
        intervals_at_fret = [(open_note + fret - key_as_int) % 12 for open_note in self.tuning]
        for pedal in pedals:
            if pedal.name not in pedals_as_str:
                raise ValueError("Invalid pedal")
            for change in pedal.changes:
                intervals_at_fret[change[0]] = (intervals_at_fret[change[0]] + change[1]) % 12

        return intervals_at_fret

    @staticmethod
    def convert_fretboard_scale_to_intervals(key: str, fretboard_scale: list[list[Optional[int]]], pedals_to_apply: Optional[list[Pedal]] = None) -> list[list[Optional[str]]]:
        fretboard_scale_as_intervals: list[Any] = copy(fretboard_scale)
        key_as_int = convert_str_note_to_int(key)

        for i_string, string_scale in enumerate(fretboard_scale_as_intervals):
            for i_fret, note in enumerate(string_scale):
                if note is not None:

                    # apply shift from pedal
                    actual_note = note
                    if pedals_to_apply:
                        for pedal in pedals_to_apply:
                            for change in pedal.changes:
                                if change[0] == i_string:
                                    actual_note += change[1]

                    interval = (actual_note - key_as_int) % 12 + 1
                    string_scale[i_fret] = convert_int_interval_to_str(interval)

        return fretboard_scale_as_intervals
