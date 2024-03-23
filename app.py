from flask import Flask, render_template, request
from fretboard.fretboard import *
from fretboard.chord_importer import import_e9_chords_from_json

from pathlib import Path

app = Flask(__name__)


# fretboard = Fretboard.init_as_guitar_standard()
# fretboard = Fretboard.init_as_guitar_open_e()

e9_chords_json_file = Path("data/E9_Chords.json")
e9_chords = import_e9_chords_from_json(e9_chords_json_file)

fretboard = Fretboard.init_as_pedal_steel_e9()
keys: list[str] = convert_int_notes_to_str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], as_sharps=True)
initial_key = "E"


def generate_scale(key: str):
    start_fret = 0
    end_fret = 12
    # fretboard_data = fretboard.generate_major_scale_as_integers(key, start_fret, end_fret)
    chord_nb = 5
    voicing_nb = 1
    fretboard_data = fretboard.generate_voicing(e9_chords[chord_nb].voicings[voicing_nb])
    pedals_to_apply = [Pedal.init_from_name(pedal) for pedal in e9_chords[chord_nb].voicings[voicing_nb].pedals]
    pedals_as_str = e9_chords[chord_nb].voicings[voicing_nb].pedals

    fretboard_data = fretboard.convert_fretboard_scale_to_intervals(key, fretboard_data, pedals_to_apply)

    return fretboard_data, pedals_as_str


@app.route("/", methods=["GET", "POST"])
def display_fretboard():

    current_key = initial_key

    if request.method == "POST":
        current_key = request.form.get("key")
        if not current_key:
            current_key = "E"

    fretboard_data, pedals_as_str = generate_scale(current_key)

    return render_template(
        "fretboard.html",
        tuning=fretboard.get_tuning_as_str(),
        fretboard_data=fretboard_data,
        nb_strings=len(fretboard_data),
        keys=keys,
        current_key=current_key,
        pedals_to_apply=pedals_as_str,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
