from ..GameState import GameState, Coordinate, Connection, Bounds


def copy_connections(
    connections: dict[Coordinate, Connection]
) -> dict[Coordinate, Connection]:
    return {
        Coordinate(anchor.x, anchor.y): Connection(
            connection.max_count,
            [Coordinate(c.x, c.y) for c in connection.connected],
        )
        for anchor, connection in connections.items()
    }
