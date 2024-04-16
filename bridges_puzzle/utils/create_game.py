from functools import reduce
from random import randint, seed
from typing import Generator, Callable

from ..GameState import Coordinate, Bounds, Connection, GameState
from .is_intersecting import is_intersecting
from .copy_connections import copy_connections
from .connect import connect


class NotEnoughSpaceError(Exception):
    message = "Not enough space to place all anchors. Consider increasing the bounds, or reducing the number of anchors."
    seed: int | float | str | bytes | bytearray | None = None
    target_anchor_count: int = 0
    placed_anchor_count: int = 0
    bounds: Bounds = Bounds(0, 0, 0, 0)
    state: GameState | None = None


def create_game(
    anchor_count: int,
    bounds: Bounds,
    difficulty: int = 0,
    seed_value: int | float | str | bytes | bytearray | None = None,
) -> GameState:
    """Creates a game state with the given anchor count and bounds.

    Args:
        anchor_count (int): The number of anchors to place.
        bounds (Bounds): The bounds of the game.
        difficulty (int, optional): The difficulty of the game. Defaults to 0. Available values are [0, 9].
        seed_value (int | float | str | bytes | bytearray | None, optional): The seed value for the random number generator. Defaults to None.

    Raises:
        ValueError: Error raised when create parameters are invalid.
        NotEnoughSpaceError: Error raised when there is not enough space to place all anchors using the current bounds, anchor count and seed value.

    Returns:
        GameState: The game state.
    """
    seed(seed_value)

    if anchor_count < 4:
        raise ValueError("Invalid anchor count. Must be at least 4.")

    available_anchors = [
        Coordinate(
            randint(bounds.left, bounds.right), randint(bounds.bottom, bounds.top)
        )
    ]

    connections = {available_anchors[0]: Connection(8, [])}
    anchor_left = anchor_count - 1

    while anchor_left > 0 and len(available_anchors) > 0:
        expandable_anchor = available_anchors[randint(0, len(available_anchors) - 1)]

        non_intersecting_coords = get_non_intersecting_coords(
            expandable_anchor, connections, bounds
        )

        if len(non_intersecting_coords) == 0:
            available_anchors.remove(expandable_anchor)
            continue

        new_anchor = non_intersecting_coords[
            randint(0, len(non_intersecting_coords) - 1)
        ]

        connections[new_anchor] = Connection(8, [])
        connections = connect(connections, expandable_anchor, new_anchor)

        unique_connections = len(
            reduce(
                lambda acc, c: acc + [c] if c not in acc else acc,
                connections[expandable_anchor].connected,
                [],
            )
        )

        if unique_connections == 4:
            available_anchors.remove(expandable_anchor)

        available_anchors.append(new_anchor)

        anchor_left -= 1

    connections = duplicate_random_connections(connections, difficulty)
    connections = sync_max_connections_to_current(connections)

    if anchor_left > 0:
        raise NotEnoughSpaceError(
            NotEnoughSpaceError.message,
            seed_value,
            anchor_count,
            anchor_count - anchor_left,
            bounds,
            GameState(connections, bounds),
        )

    return GameState(connections, bounds)


def bounded_main_cross(
    coord: Coordinate, bounds: Bounds
) -> Generator[Coordinate, None, None]:
    hcoords = [
        Coordinate(x, coord.y)
        for x in range(bounds.left, bounds.right + 1)
        if x != coord.x
    ]

    vcoords = [
        Coordinate(coord.x, y)
        for y in range(bounds.bottom, bounds.top + 1)
        if y != coord.y
    ]

    return (c for c in hcoords + vcoords)


def get_free_space_checker(
    coords_and_connections: tuple[Coordinate, Connection]
) -> Callable[[Coordinate], bool]:
    coords, connections = coords_and_connections

    def is_left(c: Coordinate) -> bool:
        return c.x < coords.x and c.y == coords.y

    def is_right(c: Coordinate) -> bool:
        return c.x > coords.x and c.y == coords.y

    def is_top(c: Coordinate) -> bool:
        return c.x == coords.x and c.y > coords.y

    def is_bottom(c: Coordinate) -> bool:
        return c.x == coords.x and c.y < coords.y

    has_left = any(is_left(c) for c in connections.connected)
    has_right = any(is_right(c) for c in connections.connected)
    has_top = any(is_top(c) for c in connections.connected)
    has_bottom = any(is_bottom(c) for c in connections.connected)

    def is_valid(c: Coordinate) -> bool:
        if is_left(c):
            return not has_left
        if is_right(c):
            return not has_right
        if is_top(c):
            return not has_top
        if is_bottom(c):
            return not has_bottom
        return False

    return is_valid


def get_non_intersecting_coords(
    target: Coordinate, connections: dict[Coordinate, Connection], bounds: Bounds
) -> list[Coordinate]:
    is_in_free_space = get_free_space_checker((target, connections[target]))
    non_intersecting_coords = []
    existing_lines = [
        (anchor, other_anchor)
        for anchor, connecting_anchors in connections.items()
        if anchor != target
        for other_anchor in connecting_anchors.connected
        if other_anchor != target
    ]

    for c in bounded_main_cross(target, bounds):
        if c in connections[target].connected:
            continue

        new_line = (target, c)

        if any(
            is_intersecting(new_line, existing_line) for existing_line in existing_lines
        ):
            continue

        if not is_in_free_space(c):
            continue

        non_intersecting_coords.append(c)

    return non_intersecting_coords


def duplicate_random_connections(
    connections: dict[Coordinate, Connection],
    difficulty: int = 0,
) -> dict[Coordinate, Connection]:
    """Randomly picks a random number of anchor and upgrade a random connection of it to a duplicated connection.

    Args:
        connections (dict[Coordinate, Connection]): The connections dictionary.
        difficulty (int, optional): How many of the anchors will be upgraded. Defaults to 1. Available values are [0, 9].

    Returns:
        dict[Coordinate, Connection]: The connections dictionary with the duplicated connections.
    """
    if difficulty < 0 or difficulty > 9:
        raise ValueError("Invalid difficulty. Must be between 0 and 9.")

    new_connections = copy_connections(connections)

    if difficulty == 0:
        return new_connections

    upgradable_anchors = [
        anchor for anchor in connections.keys() if randint(1, 9) <= difficulty
    ]

    for anchor in upgradable_anchors:
        connection = new_connections[anchor]

        if len(connection.connected) == 0:
            continue

        single_connected = [
            c for c in connection.connected if connection.connected.count(c) == 1
        ]

        if len(single_connected) == 0:
            continue

        random_anchor = single_connected[randint(0, len(single_connected) - 1)]
        new_connections = connect(new_connections, anchor, random_anchor)

    return new_connections


def sync_max_connections_to_current(
    connections: dict[Coordinate, Connection]
) -> dict[Coordinate, Connection]:
    """Make the current number of connections equal to the maximum number of connections.

    Args:
        connections (dict[Coordinate, Connection]): The connections dictionary.

    Returns:
        dict[Coordinate, Connection]: The connections dictionary with the synced connections.
    """
    new_connections: dict[Coordinate, Connection] = {}

    for anchor, connection in connections.items():
        new_connections[anchor] = Connection(
            len(connection.connected), connection.connected
        )

    return new_connections
