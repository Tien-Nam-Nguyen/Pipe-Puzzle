from typing import NamedTuple, Self


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

    def __hash__(self):
        return hash((self.right, self.top, self.left, self.bottom))

    def __eq__(self, other: Self) -> bool:
        return (
            self.right == other.right
            and self.top == other.top
            and self.left == other.left
            and self.bottom == other.bottom
        )

    def __str__(self):
        return f"Bounds(right={self.right}, top={self.top}, left={self.left}, bottom={self.bottom})"


class Connection(NamedTuple):
    max_count: int
    connected: list[Coordinate]

    def __str__(self):
        if len(self.connected) < 5:
            return f"Connection(max_count={self.max_count}, connected={self.connected})"

        return f"Connection(max_count={self.max_count}, num_of_connections={len(self.connected)})"

    def __hash__(self):
        return hash((self.max_count, len(self.connected.keys())))

    def __eq__(self, other: Self) -> bool:
        if self.max_count != other.max_count:
            return False

        if len(self.connected) != len(other.connected):
            return False

        for coord in self.connected:
            if coord not in other.connected:
                return False

        return True


class GameState(NamedTuple):
    connections: dict[Coordinate, Connection]
    bounds: Bounds

    def __str__(self):
        if len(self.connections) < 5:
            return f"GameState(connections={self.connections}, bounds={self.bounds})"

        return f"GameState(num_of_connections={len(self.connections)}, bounds={self.bounds})"

    def __hash__(self):
        return hash((len(self.connections), self.bounds))

    def __eq__(self, other: Self) -> bool:
        return self.connections == other.connections and self.bounds == other.bounds
