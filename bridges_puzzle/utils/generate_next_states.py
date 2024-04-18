from typing import Generator
from itertools import combinations

from ..GameState import GameState, Coordinate
from .add_bridge import add_bridge


def generate_next_states(
    game_state: GameState,
) -> Generator[tuple[GameState, tuple[Coordinate, Coordinate]], None, None]:
    anchors = game_state.connections.keys()

    for a, b in combinations(anchors, 2):
        if a.x != b.x and a.y != b.y:
            continue

        try:
            new_state = add_bridge(game_state, a, b)
            yield (new_state, (a, b))

        except ValueError:
            pass
