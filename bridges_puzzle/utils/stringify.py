from ..GameState import GameState, Coordinate


def stringify(game_state: GameState, show_coordinates=False) -> str:
    connections, bounds = game_state
    right, top, left, bottom = bounds
    stringy = ""

    for y in range(bottom, top + 1):
        for x in range(left, right + 1):
            entry = next(
                ((a, conn) for a, conn in connections.items() if a.x == x and a.y == y),
                None,
            )

            if entry is None:
                if show_coordinates:
                    stringy += f"{Coordinate.placeholder_string()}|- "
                    continue

                stringy += "- "
                continue

            anchor, connection = entry

            if show_coordinates:
                stringy += f"{anchor}|{connection.max_count} "
                continue

            stringy += f"{connection.max_count} "

        stringy += "\n"

    return stringy
