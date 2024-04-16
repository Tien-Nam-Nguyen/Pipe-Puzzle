from functools import reduce
from random import randint, seed
from typing import Generator, Callable

from ..GameState import Coordinate, Bounds, Connection, GameState
from .is_intersecting import is_intersecting
from .connect import connect


class NotEnoughSpaceError(Exception):
    message = "Not enough space to place all anchors. Consider increasing the bounds, or reducing the number of anchors."
    seed: int | float | str | bytes | bytearray | None = None
    target_anchor_count: int = 0
    placed_anchor_count: int = 0
    bounds: Bounds = Bounds(0, 0, 0, 0)
    state: GameState | None = None


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


def create_game(
    anchor_count: int,
    bounds: Bounds,
    seed_value: int | float | str | bytes | bytearray | None = None,
) -> GameState:
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
