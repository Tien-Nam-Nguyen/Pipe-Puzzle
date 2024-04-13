from typing import Self, Sequence


class Anchor:
    @staticmethod
    def placeholder_string():
        return "-" * 16

    def __init__(
        self, x: int, y: int, target_conn_count=None, conns: list[Self] = None
    ):
        target_conn_count = target_conn_count if target_conn_count is not None else 0
        conns = conns if conns is not None else []

        if x < 0 or y < 0:
            raise ValueError("Anchor coordinates must be positive")

        if target_conn_count < 0 or target_conn_count > 4:
            raise ValueError("Anchor target connection count must be between 0 and 4")

        if len(conns) > 4:
            raise ValueError("Anchor connections must be less than or equal to 4")

        self._x = x
        self._y = y
        self._target_conn_count = target_conn_count
        self._conns = conns

    def __str__(self):
        return f"({self.x:03}, {self.y:03} -> {self.conn_count:02})"

    def __repr__(self):
        return f"Anchor({self.x}, {self.y}, {self.target_conn_count}, {self.conns})"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def conn_count(self):
        return len(self._conns)

    @property
    def target_conn_count(self):
        return self._target_conn_count

    @property
    def conns(self) -> Sequence[Self]:
        return self._conns

    @property
    def is_satisfied(self):
        return self.conn_count == self.target_conn_count

    def add_conn(self, conn: Self):
        self._conns = [*self._conns, conn]

    def remove_conn(self, conn: Self):
        self._conns = [c for c in self._conns if c != conn]
