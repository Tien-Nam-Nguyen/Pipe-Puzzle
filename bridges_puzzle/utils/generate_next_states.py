from typing import Generator
from itertools import combinations

from ..GameState import GameState, Coordinate
from .copy import copy
from .add_bridge import add_bridge


def generate_next_states(
    game_state: GameState,
) -> Generator[tuple[GameState, tuple[Coordinate, Coordinate]], None, None]:
    anchors = game_state.connections.keys()

    for a, b in combinations(anchors, 2):
        try:
            new_state = copy(game_state)
            new_state = add_bridge(new_state, a, b)
            yield (new_state, (a, b))

        except ValueError:
            pass
