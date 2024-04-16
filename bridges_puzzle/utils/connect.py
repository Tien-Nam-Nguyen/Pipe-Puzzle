from ..GameState import Coordinate, Connection
from .is_intersecting import is_intersecting


def is_same_line(a: tuple[Coordinate, Coordinate], b: tuple[Coordinate, Coordinate]):
    return a[0] == b[0] and a[1] == b[1]


def validate_non_intersecting_connection(
    connections: dict[Coordinate, Connection], a: Coordinate, b: Coordinate
) -> None:
    line = (a, b)
    checked: list[tuple[Coordinate, Coordinate]] = []

    for start_point, conns in connections.items():
        for end_point in conns.connected:
            existing_line = (start_point, end_point)

            if any(
                is_same_line(existing_line, checked_line) for checked_line in checked
            ):
                continue

            checked.append(existing_line)

            converging = line[0] == existing_line[0] or line[0] == existing_line[1]

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
        new_connections = connections.copy()
        new_connections[a].connected.append(b)
        new_connections[b].connected.append(a)
        return new_connections

    if a.x != b.x and a.y != b.y:
        message = f"Invalid connection. Coordinate {a} is not directly vertical or horizontal of {b}."
        raise ValueError(message)

    validate_non_intersecting_connection(connections, a, b)

    new_connections = connections.copy()
    new_connections[a].connected.append(b)
    new_connections[b].connected.append(a)
    return new_connections
