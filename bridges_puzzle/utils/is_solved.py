from ..GameState import GameState


def is_solved(game_state: GameState) -> bool:
    """A game state is considered solved if all connections have reached their max count.

    Args:
        game_state (GameState): The game state to check if it's solved.

    Returns:
        bool: True if all connections have reached their max count, False otherwise.
    """
    return all(
        connection.max_count == len(connection.connected)
        for connection in game_state.connections.values()
    )
