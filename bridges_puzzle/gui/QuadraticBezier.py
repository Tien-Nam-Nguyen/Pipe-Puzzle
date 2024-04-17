from pygame.draw import line, lines
from pygame.math import Vector2
from pygame.color import Color

from .GameObject import GameObject
from .utils import quadratic_bezier


class QuadraticBezier(GameObject):
    def __init__(
        self,
        step: int,
        width: int,
        start: Vector2 | None = None,
        mid: Vector2 | None = None,
        end: Vector2 | None = None,
    ) -> None:
        start = start if start is not None else Vector2(0, 0)
        mid = mid if mid is not None else Vector2(0, 0)
        end = end if end is not None else Vector2(0, 0)

        super().__init__()

        self.__step = step
        self.width = width
        self.__vertices = [start, mid, end]
        self.__render_vertices = QuadraticBezier.make_render_vertices(
            start, mid, end, step
        )

        self.__modified = False

    def set_start(self, x: float, y: float):
        self.__vertices[0].update(x, y)
        self.__modified = True

    def set_mid(self, x: float, y: float):
        self.__vertices[1].update(x, y)
        self.__modified = True

    def set_end(self, x: float, y: float):
        self.__vertices[2].update(x, y)
        self.__modified = True

    def update(self, delta_time: float, time: float):
        if not self.__modified:
            return

        self.update_render_vertices()

    def render(self, delta_time: float, time: float):
        lines(
            self.screen, Color(230, 230, 230), False, self.__render_vertices, self.width
        )
        line(
            self.screen,
            Color(230, 230, 230),
            self.__render_vertices[-1],
            self.__vertices[2],
            self.width,
        )

    def update_render_vertices(self):
        self.__modified = False
        for i in range(self.__step):
            coords = quadratic_bezier(
                self.__vertices[0],
                self.__vertices[1],
                self.__vertices[2],
                i / self.__step,
            )
            self.__render_vertices[i].update(*coords)

    @staticmethod
    def make_render_vertices(
        start: Vector2, mid: Vector2, end: Vector2, step: int
    ) -> list[Vector2]:
        ls = []

        for i in range(step):
            coords = quadratic_bezier(start, mid, end, i / step)
            ls.append(Vector2(*coords))

        return ls
