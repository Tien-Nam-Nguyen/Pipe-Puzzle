from pygame import font
from pygame.draw import rect
from pygame.time import Clock, get_ticks
from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect

from tweener import Tween, Easing, EasingMode

from .GameObject import GameObject


class Anchor(GameObject):
    def __init__(
        self,
        screen: Surface,
        clock: Clock,
        x: float,
        y: float,
        radius: float,
        anim_delay: float,
        value: float | None = None,
    ):
        super().__init__(screen, clock)
        self.x = x
        self.y = y
        self.value = value
        self.radius = radius
        self.anim_delay = anim_delay

        self.anim_radius = Tween(0, self.radius, 1000, Easing.ELASTIC, EasingMode.OUT)

    def start(self):
        self.start_time = get_ticks()

    def render(self, delta_time: float, time: float):
        if self.value is None:
            rect(
                self.screen,
                Color(230, 230, 230),
                Rect(
                    self.x - self.anim_radius.value,
                    self.y - self.anim_radius.value,
                    2 * self.anim_radius.value,
                    2 * self.anim_radius.value,
                ),
                width=2,
                border_radius=20,
            )

            return

        rect(
            self.screen,
            Color(230, 230, 230),
            Rect(
                self.x - self.anim_radius.value,
                self.y - self.anim_radius.value,
                2 * self.anim_radius.value,
                2 * self.anim_radius.value,
            ),
            border_radius=20,
        )

        fnt = font.Font(None, 36)
        text = fnt.render(
            str(self.value),
            True,
            "black",
        )
        text.set_alpha(
            min(255, int(round(self.anim_radius.value / self.radius * 255, 0)))
        )
        self.screen.blit(
            text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2)
        )

    def update(self, delta_time: float, time: float):
        if time - self.start_time > self.anim_delay:
            self.anim_radius.start()
            # set infinity so that it doesn't start again
            self.start_time = float("inf")

        if self.anim_radius.animating:
            self.anim_radius.update()
