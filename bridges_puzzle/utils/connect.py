from ..GameState import Coordinate, Connection
from .is_intersecting import is_intersecting
from .copy_connections import copy_connections


def is_same_line(a: tuple[Coordinate, Coordinate], b: tuple[Coordinate, Coordinate]):
    return (a[0] == b[0] and a[1] == b[1]) or (a[0] == b[1] and a[1] == b[0])


def is_between(coord: Coordinate, a: Coordinate, b: Coordinate):
    on_same_row = a.y == b.y and a.y == coord.y
    on_same_col = a.x == b.x and a.x == coord.x

    return (on_same_row and min(a.x, b.x) <= coord.x <= max(a.x, b.x)) or (
        on_same_col and min(a.y, b.y) <= coord.y <= max(a.y, b.y)
    )


def validate_non_intersecting_connection(
    connections: dict[Coordinate, Connection], a: Coordinate, b: Coordinate
) -> None:
    line = (a, b)
    checked: list[tuple[Coordinate, Coordinate]] = []

    for start_point, conns in connections.items():
        if start_point != a and start_point != b and is_between(start_point, a, b):
            raise ValueError(
                f"Invalid connection. Line {line} intersects with existing anchor {start_point}."
            )

        for end_point in conns.connected:
            existing_line = (start_point, end_point)

            if any(
                is_same_line(existing_line, checked_line) for checked_line in checked
            ):
                continue

            checked.append(existing_line)

            converging = (
                line[0] == existing_line[0]
                or line[0] == existing_line[1]
                or line[1] == existing_line[0]
                or line[1] == existing_line[1]
            )

            if not converging and is_intersecting(line, existing_line):
                message = f"Invalid connection. Line {line} intersects with existing line {existing_line}."
                raise ValueError(message)


def connect(
    connections: dict[Coordinate, Connection], a: Coordinate, b: Coordinate
) -> dict[Coordinate, Connection]:
    if len(connections[a].connected) >= connections[a].max_count:
        message = f"Invalid connection. Coordinate {a} already has the maximum number of connections."
        raise ValueError(message)

    if len(connections[b].connected) >= connections[b].max_count:
        message = f"Invalid connection. Coordinate {b} already has the maximum number of connections."
        raise ValueError(message)

    existing_connections = connections[a].connected.count(b)

    if existing_connections >= 2:
        message = f"Invalid connection. Coordinate {a} and {b} are already connected by 2 bridges."
        raise ValueError(message)

    if existing_connections == 1:
        new_connections = copy_connections(connections)
        new_connections[a].connected.append(b)
        new_connections[b].connected.append(a)
        return new_connections

    if a.x != b.x and a.y != b.y:
        message = f"Invalid connection. Coordinate {a} is not directly vertical or horizontal of {b}."
        raise ValueError(message)

    validate_non_intersecting_connection(connections, a, b)

    new_connections = copy_connections(connections)
    new_connections[a].connected.append(b)
    new_connections[b].connected.append(a)
    return new_connections
