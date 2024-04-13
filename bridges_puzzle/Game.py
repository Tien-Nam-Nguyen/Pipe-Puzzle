from functools import reduce
from typing import Sequence, NamedTuple
from .Anchor import Anchor


class Bounds(NamedTuple):
    right: int
    top: int
    left: int
    bottom: int


class Game:
    def __init__(self, anchor_count: int):
        self.anchors: list[Anchor] = []

        for i in range(anchor_count):
            self.anchors.append(Anchor(i, i, i))


def calc_bounding_box(anchors: Sequence[Anchor]) -> Bounds:
    return reduce(
        lambda acc, anchor: (
            max(acc[0], anchor.x),
            min(acc[1], anchor.y),
            min(acc[2], anchor.x),
            max(acc[3], anchor.y),
        ),
        anchors,
        Bounds(0, 0, 0, 0),
    )


def print_game_state(anchors: Sequence[Anchor]) -> str:
    right, top, left, bottom = calc_bounding_box(anchors)
    stringy = ""

    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            anchor = next((a for a in anchors if a.x == x and a.y == y), None)

            if anchor is not None:
                stringy += f"{anchor} "
            else:
                stringy += f"{Anchor.placeholder_string()} "

        stringy += "\n"

    return stringy
