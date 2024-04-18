from typing import NamedTuple, Generator

from .is_solved import is_solved
from .generate_next_states import generate_next_states
from ..GameState import GameState, Coordinate, Connection


class AStarSolution(NamedTuple):
    states: list[GameState]
    moves: list[tuple[Coordinate, Coordinate]]


class NoSolutionFound(Exception):
    game_state: GameState
    message = "No solution found"

    def __init__(self, game_state: GameState, *args: object) -> None:
        super().__init__(*args)
        self.game_state = game_state


def get_count_of_free_directions(coords: Coordinate, connections: Connection) -> int:
    def is_left(c: Coordinate) -> bool:
        return c.x < coords.x and c.y == coords.y

    def is_right(c: Coordinate) -> bool:
        return c.x > coords.x and c.y == coords.y

    def is_top(c: Coordinate) -> bool:
        return c.x == coords.x and c.y > coords.y

    def is_bottom(c: Coordinate) -> bool:
        return c.x == coords.x and c.y < coords.y

    available_directions = [is_left, is_right, is_top, is_bottom]

    for connection in connections.connected:
        if len(available_directions) == 0:
            return 0

        for is_in_this_direction in available_directions:
            if is_in_this_direction(connection):
                available_directions.remove(is_in_this_direction)
                break

    return len(available_directions)


def get_count_of_existing_connections(game_state: GameState) -> int:
    skippable = []
    count = 0
    for coords, conn in game_state.connections.items():
        for connection in conn.connected:
            if (coords, connection) in skippable:
                continue

            count += 1
            skippable.append((connection, coords))

    return count


def get_heuristic(game_state: GameState) -> float:
    un_satisfied_anchors = [
        anchor
        for anchor, connections in game_state.connections.items()
        if len(connections.connected) != connections.max_count
    ]

    if len(un_satisfied_anchors) == 0:
        return float("-inf")

    return sum(c.max_count - len(c.connected) for c in game_state.connections.values())


class Node(NamedTuple):
    f: float
    g: float
    h: float
    state: GameState


def insert_sorted(sorted_list: list[Node], item: Node) -> None:
    """Insert an item into a list that's already sorted from lowest to highest.

    Args:
        sorted_list (list[tuple[int, GameState]]): A list of tuples where the first element is an integer.
        item (tuple[int, GameState]): A tuple to insert into the list.
    """

    for i, node in enumerate(sorted_list):
        if item.f <= node.f:
            sorted_list.insert(i, item)
            return

    sorted_list.append(item)


DEPTH_WEIGHT = 1


def a_star(game_state: GameState) -> AStarSolution:
    state_list: list[Node] = [Node(0, 0, get_heuristic(game_state), game_state)]
    trace = {game_state: None}

    while state_list:
        _, g, h, solution = state_list.pop(0)

        if is_solved(solution):
            states = [solution]
            moves = []

            while trace[solution]:
                prev_solution, move = trace[solution]
                states.insert(0, prev_solution)
                moves.insert(0, move)
                solution = prev_solution

            return AStarSolution(states, moves)

        states_and_moves = [ss for ss in generate_next_states(solution)]
        hs = [get_heuristic(ss) for ss, _ in states_and_moves]

        for (state, move), h in zip(states_and_moves, hs):
            if state not in trace:
                new_g = g + DEPTH_WEIGHT
                new_f = new_g + h
                insert_sorted(state_list, Node(new_f, new_g, h, state))
                trace[state] = (solution, move)

    raise NoSolutionFound(game_state)
