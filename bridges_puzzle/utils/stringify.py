from ..GameState import GameState, Coordinate


def stringify(game_state: GameState) -> str:
    connections, bounds = game_state
    right, top, left, bottom = bounds
    stringy = ""

    for y in range(bottom, top + 1):
        for x in range(left, right + 1):
            anchor = next(
                (a for a in connections.keys() if a.x == x and a.y == y), None
            )

            if anchor is not None:
                stringy += f"{anchor} "
            else:
                stringy += f"{Coordinate.placeholder_string()} "

        stringy += "\n"

    return stringy
