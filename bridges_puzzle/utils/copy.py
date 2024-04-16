from ..GameState import GameState, Coordinate, Connection, Bounds


def copy(game_state: GameState) -> GameState:
    connections, bounds = game_state
    return GameState(
        connections={
            Coordinate(anchor.x, anchor.y): Connection(
                connection.max_count,
                [Coordinate(c.x, c.y) for c in connection.connected],
            )
            for anchor, connection in connections.items()
        },
        bounds=Bounds(*bounds),
    )
