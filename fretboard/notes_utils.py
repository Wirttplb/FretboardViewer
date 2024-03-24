MUTED_STRING_CHAR: str = "x"


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
    reversed_interval_map = {0: "1", 1: "b2", 2: "2", 3: "b3", 4: "3", 5: "4", 6: "b5", 7: "5", 8: "b6", 9: "6", 10: "b7", 11: "7"}

    if note in reversed_interval_map:
        return reversed_interval_map[note]
    else:
        raise ValueError("Invalid interval value!")


def convert_str_interval_to_int(interval: str) -> int:
    interval_map = {"1": 0, "b2": 1, "2": 2, "b3": 3, "3": 4, "4": 5, "b5": 6, "5": 7, "#5": 7, "b6": 8, "6": 9, "bb7": 9, "b7": 10, "7": 11, "9": 2, "11": 5, "13": 9}

    if interval in interval_map:
        return interval_map[interval]
    else:
        raise ValueError("Invalid interval name!")
