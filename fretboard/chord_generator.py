from copy import copy
import numpy as np
from typing import Optional

from fretboard.chords import Chord, Voicing
from fretboard.fretboard import Fretboard
from fretboard.pedal import Pedal, E9_PEDAL_CHANGES

from fretboard.notes_utils import convert_str_interval_to_int

CHORD_FORMULAS: dict[str, list[str]] = {
    "M": ["1", "3", "5"],
    "m": ["1", "b3", "5"],
    "m7": ["1", "b3", "5", "b7"],
    "M7": ["1", "3", "5", "7"],
    "sus2": ["1", "2", "5"],
    "sus4": ["1", "4", "5"],
    "add9": ["1", "2", "3", "5"],
    "madd9": ["1", "2", "b3", "5"],
    "7": ["1", "3", "5", "b7"],
    "M6": ["1", "3", "5", "6"],
    "aug": ["1", "3", "#5"],
    "dim": ["1", "b3", "b5"],
    "Mb5": ["1", "3", "b5"],
    "m7b5": ["1", "b3", "b5", "b7"],
    "mb5bb7": ["1", "b3", "b5", "bb7"],
    "M6add9": ["1", "2", "3", "5", "6"],
    "M7/6": ["1", "3", "5", "7", "6"],
    "mm6": ["1", "b3", "5", "b6"],
    "mM6": ["1", "b3", "5", "6"],
    "M9": ["1", "3", "5", "7", "2"],
    "9": ["1", "3", "5", "b7", "9"],
    "7b9": ["1", "3", "5", "b7", "b2"],
    "7#9": ["1", "3", "5", "b7", "b3"],
    "m9": ["1", "b3", "5", "b7", "b2"],
    "mM9": ["1", "b3", "5", "b7", "2"],
    "b5b13": ["1", "3", "b5", "b6"],
    "11": ["1", "3", "5", "7", "2", "4"],
    "13": ["1", "3", "5", "7", "2", "4", "6"],
}


class ChordGenerator:

    fretboard: Fretboard

    def __init__(self, fretboard: Fretboard):
        self.fretboard = fretboard

    def generate_voicings(self, formula: list[str], key: str) -> list[Voicing]:

        formula_as_int = [convert_str_interval_to_int(note) for note in formula]
        pedal_combinations = self.fretboard.get_all_pedal_combinations()
        voicings: list[Voicing] = []

        # loop on frets to find voicings
        for fret in range(0, 12):

            # loop on pedals to try all combinations
            for pedal_combination in pedal_combinations:
                pedals_to_apply: list[Pedal] = [Pedal.init_from_name(pedal_as_str) for pedal_as_str in pedal_combination]
                intervals_at_fret = self.fretboard.get_intervals_at_fret(fret, pedals_to_apply, key=key)

                # Check chord is actually complete
                chord_not_complete = False
                for interval in formula_as_int:
                    if interval not in intervals_at_fret:
                        chord_not_complete = True
                        break

                if chord_not_complete:
                    continue

                # Keep only strings actually played
                voicing = Voicing()
                voicing.pedals = pedal_combination
                voicing.notes = copy(intervals_at_fret)  # type: ignore
                for i, _ in enumerate(voicing.notes):
                    if voicing.notes[i] in formula_as_int:
                        voicing.notes[i] = fret
                    else:
                        voicing.notes[i] = None  # type: ignore

                # Check if all pedals are actually necessary for this voicing
                pedal_not_necessary = False
                for pedal in pedals_to_apply:
                    has_necessary_change = False
                    for change in pedal.changes:
                        if voicing.notes[change[0]] is not None:  # string number
                            has_necessary_change = True
                            break

                    if has_necessary_change == False:
                        pedal_not_necessary = True

                    if pedal_not_necessary:
                        break

                if pedal_not_necessary:
                    continue

                voicings.append(voicing)

        return voicings

    @staticmethod
    def generate_e9_chords(key_as_str: str) -> dict[str, Chord]:
        """Return dict of e9 chords with associated voicings

        Returns:
            dict[str, Chord]: chords
        """
        chord_generator = ChordGenerator(Fretboard.init_as_pedal_steel_e9())
        chords: dict[str, Chord] = {}

        for key, value in CHORD_FORMULAS.items():
            chords[key] = Chord(key=key_as_str, type=key)
            chords[key].voicings = chord_generator.generate_voicings(value, key_as_str)

        return chords

    @staticmethod
    def generate_open_e_chords(key_as_str: str) -> dict[str, Chord]:
        """Return dict of open e chords with associated voicings

        Returns:
            dict[str, Chord]: chords
        """
        chord_generator = ChordGenerator(Fretboard.init_as_guitar_open_e())
        chords: dict[str, Chord] = {}

        for key, value in CHORD_FORMULAS.items():
            chords[key] = Chord(key=key_as_str, type=key)
            chords[key].voicings = chord_generator.generate_voicings(value, key_as_str)

        return chords
