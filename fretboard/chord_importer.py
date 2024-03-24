from fretboard.chords import Chord, Voicing

from pathlib import Path
import json


@staticmethod
def import_e9_chords_from_json(filepath: Path) -> list[Chord]:

    with open(filepath) as file:
        data = json.load(file)

    chords: list[Chord] = []

    for chord_json in data["chords"]:
        chord = Chord(key="E", type=chord_json["type"])

        for voicing_json in chord_json["voicings"]:
            voicing = Voicing.from_e9_json(voicing_json)
            chord.voicings.append(voicing)

        chords.append(chord)

    return chords
