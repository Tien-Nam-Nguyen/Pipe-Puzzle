from .copy_connections import copy_connections
from ..GameState import GameState, Coordinate, Connection, Bounds


def copy(game_state: GameState) -> GameState:
    connections, bounds = game_state
    copied = copy_connections(connections)

    return GameState(
        connections=copied,
        bounds=Bounds(*bounds),
    )
