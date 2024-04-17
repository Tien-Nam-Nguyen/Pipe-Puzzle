from pygame.mouse import get_pos
from pygame.math import Vector2

from .GameObject import GameObject
from .QuadraticBezier import QuadraticBezier
from .Dynamics import Dynamics, DynamicsConfig


class Wire(GameObject):
    def __init__(self, x: float, y: float, stretch_length: float):
        super().__init__()

        self.x = x
        self.y = y

        self.target_x = 0
        self.target_y = 0
        self.droop = 0
        self.stretch_length = stretch_length

        self.mid_x, self.mid_y = Wire.get_mid_pos(
            (self.x, self.y), (self.target_x, self.target_y), self.droop
        )

        self.interpolators = {
            "x": Dynamics(self.x, DynamicsConfig(1, 0.45, 2)),
            "y": Dynamics(self.y, DynamicsConfig(3, 0.45, 2)),
        }

        self.i_mid_x, self.i_mid_y = self.mid_x, self.mid_y

        self.bezier = QuadraticBezier(
            20,
            5,
            Vector2(self.x, self.y),
            Vector2(self.mid_x, self.mid_y),
            Vector2(self.target_x, self.target_y),
        )

    def update(self, delta_time: float, time: float):
        mouse_pos = get_pos()

        self.target_x = mouse_pos[0]
        self.target_y = mouse_pos[1]

        self.droop = max(self.stretch_length - abs(self.target_x - self.x), 0.0)

        self.mid_x, self.mid_y = Wire.get_mid_pos(
            (self.x, self.y), (self.target_x, self.target_y), self.droop
        )

        self.i_mid_x = self.interpolators["x"].get_interpolated(delta_time, self.mid_x)
        self.i_mid_y = self.interpolators["y"].get_interpolated(delta_time, self.mid_y)

        self.bezier.set_start(self.x, self.y)
        self.bezier.set_mid(self.i_mid_x, self.i_mid_y)
        self.bezier.set_end(self.target_x, self.target_y)
        self.bezier.update(delta_time, time)

    def render(self, delta_time: float, time: float):
        self.bezier.render(delta_time, time)

    @staticmethod
    def get_mid_pos(start: tuple[float, float], end: tuple[float, float], droop: float):
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        mid_y += droop

        return mid_x, mid_y
