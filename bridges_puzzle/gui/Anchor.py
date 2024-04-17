from pygame import font
from pygame.draw import rect
from pygame.time import Clock, get_ticks
from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect

from tweener import Tween, Easing, EasingMode, Ease

from .GameObject import GameObject
from .Button import ButtonEvents
from .ScaleButton import ScaleButton


class Anchor(GameObject):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        anim_delay: float,
        value: float | None = None,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.value = value
        self.radius = 0.0
        self.anim_delay = anim_delay

        self.anim_appear_radius = Tween(0, radius, 1000, Easing.ELASTIC, EasingMode.OUT)
        self.rect = Rect(x - radius, y - radius, 2 * radius, 2 * radius)

        self.button = ScaleButton(self.rect, 1.2, 1.3)

    def start(self):
        self.start_time = get_ticks()
        self.button.on(ButtonEvents.CLICK, lambda: print(f"clicked {self.value}"))

    def render(self, delta_time: float, time: float):
        if self.value is None:
            rect(
                self.screen,
                Color(230, 230, 230),
                self.rect,
                width=2,
                border_radius=20,
            )

            return

        rect(
            self.screen,
            Color(230, 230, 230),
            self.rect,
            border_radius=20,
        )

        fnt = font.Font(None, 36)
        text = fnt.render(
            str(self.value),
            True,
            "black",
        )
        text.set_alpha(
            min(
                255,
                int(
                    round(
                        self.anim_appear_radius.value / max(self.radius, 0.01) * 255, 0
                    )
                ),
            )
        )
        self.screen.blit(
            text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2)
        )

    def update(self, delta_time: float, time: float):
        if time - self.start_time > self.anim_delay:
            self.anim_appear_radius.start()
            # set infinity so that it doesn't start again
            self.start_time = float("inf")

        if self.anim_appear_radius.animating:
            self.anim_appear_radius.update()
            self.radius = self.anim_appear_radius.value
            self.rect.update(
                self.x - self.radius,
                self.y - self.radius,
                2 * self.radius,
                2 * self.radius,
            )

            return

        self.button.update(delta_time, time)
        rect = self.button.scaled_rect
        self.rect.update(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
        )
