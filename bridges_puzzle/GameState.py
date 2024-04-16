from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x:02}, {self.y:02})"

    @staticmethod
    def placeholder_string():
        return "-" * 8


class Bounds(NamedTuple):
    right: int
    top: int
    left: int
    bottom: int


class Connection(NamedTuple):
    max_count: int
    connected: list[Coordinate]


class GameState(NamedTuple):
    connections: dict[Coordinate, Connection]
    bounds: Bounds

    def __str__(self):
        if len(self.connections) < 5:
            return f"GameState(connections={self.connections}, bounds={self.bounds})"

        return f"GameState(num_of_connections={len(self.connections)}, bounds={self.bounds})"
