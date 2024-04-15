from __future__ import annotations
from typing import Optional


from fretboard.notes_utils import convert_int_interval_to_str, convert_str_note_to_int, MUTED_STRING_CHAR
from fretboard.pedal import Pedal


class Voicing:
    """Representation of a chord voicing"""

    pedals: list[str] = []
    notes: list[Optional[int]] = []  # as fret number, or None ; one for each string

    def __init__(self):
        self.pedals = []
        self.notes = []

    @staticmethod
    def from_e9_json(voicing_json: dict) -> Voicing:
        voicing = Voicing()
        voicing.pedals = voicing_json["pedals"]
        for json_note in voicing_json["notes"]:
            voicing.notes.append(int(json_note) if json_note != MUTED_STRING_CHAR else None)

        return voicing

    def get_number_of_notes(self) -> int:
        n = 0
        for note in self.notes:
            if note is not None:
                n += 1
        return n
    
    def is_part_of_other_voicing(self, other: Voicing) -> bool:
        """Returns true if voicing is already a part of another voicing
        """
        for pedal in self.pedals:
            if pedal not in other.pedals:
                return False
            
        for i, note in enumerate(self.notes):
            if note is not None and other.notes[i] is None:
                return False
            if note is not None and other.notes[i] is not None and note != other.notes[i]:
                return False
            
        return True
    
    def is_part_of_other_voicings(self, others: list[Voicing]) -> bool:
        for other in others:
            if self != other and self.is_part_of_other_voicing(other):
                return True
            
        return False
            



class Chord:
    """Representation of a chord and associated voicings"""

    key: str = ""
    type: str = ""
    voicings: list[Voicing] = []

    def __init__(self, key: str, type: str):
        self.key = key
        self.type = type
        self.voicings = []

    def to_json(self, tuning: list[int]) -> dict:
        json_dict = {}
        json_dict["name"] = self.type
        json_dict["voicings"] = []

        key_as_int = convert_str_note_to_int(self.key)

        for voicing in self.voicings:
            voicing_dict = {}
            voicing_dict["pedals"] = voicing.pedals
            voicing_dict["notes"] = [note if note is not None else MUTED_STRING_CHAR for note in voicing.notes]
            voicing_dict["intervals"] = [(note + tuning[i_string] - key_as_int) % 12 if note is not None else None for i_string, note in enumerate(voicing.notes)]

            # Apply pedal change
            for pedal in voicing.pedals:
                pedal_object = Pedal.init_from_name(pedal)

                for i, _ in enumerate(voicing_dict["intervals"]):
                    for change in pedal_object.changes:
                        if change[0] == i:

                            if voicing_dict["intervals"][i] is not None:
                                voicing_dict["intervals"][i] = (voicing_dict["intervals"][i] + change[1]) % 12  # type:ignore

            voicing_dict["intervals"] = [convert_int_interval_to_str(interval) if interval is not None else MUTED_STRING_CHAR for interval in voicing_dict["intervals"]]

            json_dict["voicings"].append(voicing_dict)

        return json_dict

    @staticmethod
    def list_to_json(chords: dict[str, Chord], tuning: list[int]) -> dict:
        json_dict = {}
        json_dict["chords"] = []
        for chord in chords.values():
            json_dict["chords"].append(chord.to_json(tuning))

        return json_dict
