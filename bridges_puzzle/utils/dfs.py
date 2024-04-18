from typing import NamedTuple

from .is_solved import is_solved
from .generate_next_states import generate_next_states
from ..GameState import GameState, Coordinate


class DFSSolution(NamedTuple):
    states: list[GameState]
    moves: list[tuple[Coordinate, Coordinate]]


class NoSolutionFound(Exception):
    game_state: GameState
    message = "No solution found"

    def __init__(self, game_state: GameState, *args: object) -> None:
        super().__init__(*args)
        self.game_state = game_state


def dfs(game_state: GameState) -> DFSSolution:
    stack = [game_state]
    trace = {game_state: None}

    while stack:
        solution = stack.pop()

        if is_solved(solution):
            states = [solution]
            moves = []

            while trace[solution]:
                prev_solution, move = trace[solution]
                states.insert(0, prev_solution)
                moves.insert(0, move)
                solution = prev_solution

            return DFSSolution(states, moves)

        for next_state, move in generate_next_states(solution):
            if next_state not in trace:
                stack.append(next_state)
                trace[next_state] = (solution, move)

    raise NoSolutionFound(game_state)
