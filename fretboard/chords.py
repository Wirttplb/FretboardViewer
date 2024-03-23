from __future__ import annotations
from typing import Optional


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
            voicing.notes.append(int(json_note) if json_note != "x" else None)

        return voicing


class Chord:
    """Representation of a chord and associated voicings"""

    type: str = ""
    voicings: list[Voicing] = []

    def __init__(self):
        self.type = ""
        self.voicings = []
