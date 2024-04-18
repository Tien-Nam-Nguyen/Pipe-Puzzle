from typing import NamedTuple

from .is_solved import is_solved
from .generate_next_states import generate_next_states
from ..GameState import GameState, Coordinate


class BFSSolution(NamedTuple):
    states: list[GameState]
    moves: list[tuple[Coordinate, Coordinate]]


class NoSolutionFound(Exception):
    game_state: GameState
    message = "No solution found"

    def __init__(self, game_state: GameState, *args: object) -> None:
        super().__init__(*args)
        self.game_state = game_state


def bfs(game_state: GameState) -> BFSSolution:
    queue = [game_state]
    trace = {game_state: None}

    while queue:
        solution = queue.pop(0)

        if is_solved(solution):
            states = [solution]
            moves = []

            while trace[solution]:
                prev_solution, move = trace[solution]
                states.insert(0, prev_solution)
                moves.insert(0, move)
                solution = prev_solution

            return BFSSolution(states, moves)

        for next_state, move in generate_next_states(solution):
            if next_state not in trace:
                queue.append(next_state)
                trace[next_state] = (solution, move)

    raise NoSolutionFound(game_state)
