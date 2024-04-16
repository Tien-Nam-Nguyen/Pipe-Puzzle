from .connect import connect
from ..GameState import GameState, Coordinate


def add_bridge(game_state: GameState, a: Coordinate, b: Coordinate) -> GameState:
    connections, bounds = game_state
    connections = connect(connections, a, b)
    return GameState(connections, bounds)
