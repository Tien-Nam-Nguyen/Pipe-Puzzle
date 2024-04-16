from pygame import font
from pygame.draw import line
from pygame.time import Clock, get_ticks
from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect

from tweener import Tween, Easing, EasingMode

from .GameObject import GameObject


class Bridge(GameObject):
    def __init__(
        self,
        screen: Surface,
        clock: Clock,
        start: tuple[float, float],
        end: tuple[float, float],
        anim_delay: float,
        double=False,
    ):
        super().__init__(screen, clock)
        self.start_node = start
        self.end_node = end
        self.double = double
        self.anim_delay = anim_delay

        self.anim_thickness = Tween(0, 10, 1000, Easing.EXPO, EasingMode.IN_OUT)

    def start(self):
        self.start_time = get_ticks()

    def render(self, delta_time: float, time: float):
        if not self.double:
            line(
                self.screen,
                Color(230, 230, 230),
                self.start_node,
                self.end_node,
                int(self.anim_thickness.value),
            )

            return

        # draw double bridge
        offset = 10
        is_horizontal = self.start_node[1] == self.end_node[1]

        if is_horizontal:
            line(
                self.screen,
                Color(230, 230, 230),
                (self.start_node[0], self.start_node[1] - offset),
                (self.end_node[0], self.end_node[1] - offset),
                int(self.anim_thickness.value),
            )

            line(
                self.screen,
                Color(230, 230, 230),
                (self.start_node[0], self.start_node[1] + offset),
                (self.end_node[0], self.end_node[1] + offset),
                int(self.anim_thickness.value),
            )

            return

        line(
            self.screen,
            Color(230, 230, 230),
            (self.start_node[0] - offset, self.start_node[1]),
            (self.end_node[0] - offset, self.end_node[1]),
            int(self.anim_thickness.value),
        )

        line(
            self.screen,
            Color(230, 230, 230),
            (self.start_node[0] + offset, self.start_node[1]),
            (self.end_node[0] + offset, self.end_node[1]),
            int(self.anim_thickness.value),
        )

    def update(self, delta_time: float, time: float):
        if time - self.start_time > self.anim_delay:
            self.anim_thickness.start()
            # set infinity so that it doesn't start again
            self.start_time = float("inf")

        if self.anim_thickness.animating:
            self.anim_thickness.update()
