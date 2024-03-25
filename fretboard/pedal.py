from __future__ import annotations

import itertools

E9_PEDAL_CHANGES: dict[str, list[tuple[int, int]]] = {
    "A": [(0, 2), (5, 2)],
    "A/2": [(0, 1), (5, 1)],
    "B": [(4, 1), (7, 1)],
    "C": [(5, 2), (6, 2)],
    "E": [(2, -1), (6, -1)],
    "F": [(2, 1), (6, 1)],
    "G": [(3, 1), (9, 1)],
    "D": [(1, -1), (8, -2)],
    "D/2": [(8, -1)],
}

# PEDAL_COMBINATIONS: list[list[str]] = [["A"], ["B"], ["C"], ["A", "B"], ["B", "C"], ["E"], ["F"], ["A", "E"], ["A", "F"], ["B", "F"], ["B", "F"], ["G"], ""]


class Pedal:
    """Class representing a pedal associated to a tuning"""

    name: str = ""  # name of pedal or lever (commonly: "A", "B", "C", "E", "G", "F", "D"...)
    changes: list[tuple[int, int]] = []  # string number (from bottom, 0 to n) and interval (like +1, +2, -1 etc...)

    @staticmethod
    def init_from_name(name: str) -> Pedal:
        pedal = Pedal()
        pedal.name = name
        pedal.changes = E9_PEDAL_CHANGES[name]

        return pedal

    @staticmethod
    def get_all_pedal_combinations(pedals: list[str]) -> list[list[str]]:
        list = [[]]  # init with no pedal
        for i in range(1, 3 + 1):
            list += unique_combinations(pedals, i)

        # Delete impossible combinations
        to_delete = []
        for i, combination in enumerate(list):
            if (
                ("A" in combination and "A/2" in combination)
                or ("D" in combination and "D/2" in combination)
                or ("A" in combination and "C" in combination)
                or ("A/2" in combination and "C" in combination)
                or ("E" in combination and "F" in combination)
                or ("D" in combination and "G" in combination)
                or ("D/2" in combination and "G" in combination)
            ):
                to_delete.append(i)

        for i in sorted(to_delete, reverse=True):
            del list[i]

        return list


def unique_combinations(iterable, r):
    combinations = itertools.combinations(iterable, r)
    combinations_as_list = list(combinations)
    combinations_as_list = [list(combination_as_tuple) for combination_as_tuple in combinations_as_list]
    return combinations_as_list
