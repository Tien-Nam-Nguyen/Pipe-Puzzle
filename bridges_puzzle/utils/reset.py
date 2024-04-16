from ..GameState import GameState, Connection, Coordinate, Bounds


def reset(game_state: GameState) -> GameState:
    """Returns a deep copied game state with all connections removed.

    *Note*: Don't forget to backup the finished game state before resetting it.

    Args:
        game_state (GameState): The game state to reset.

    Returns:
        GameState: The reset game state.
    """
    connections, bounds = game_state
    return GameState(
        {
            Coordinate(coord.x, coord.y): Connection(connection.max_count, [])
            for coord, connection in connections.items()
        },
        bounds,
    )
