from pygame import font
from pygame.draw import rect
from pygame.time import Clock, get_ticks
from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect

from tweener import Tween, Easing, EasingMode, Ease

from .GameObject import GameObject
from .Button import Button, ButtonEvents


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

        anim_appear = Tween(0, radius, 1000, Easing.ELASTIC, EasingMode.OUT)
        self.anim_radius = anim_appear

        self.anim_radius_start = None
        self.anim_radius_target = None

        self.button = Button(Rect(x - radius, y - radius, 2 * radius, 2 * radius))

        self.basic_tween = Tween(0.0, 1.0, 200, Easing.QUAD, EasingMode.IN_OUT)

        enter_target = radius * 1.2
        rest_target = radius
        down_target = radius * 1.3
        up_target = radius

        def handle_click():
            pass

        def handle_down():

            self.basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.basic_tween.start()
            self.basic_tween.update()
            self.anim_radius_start = self.radius
            self.anim_radius_target = down_target

        def handle_up():

            self.basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.basic_tween.start()
            self.basic_tween.update()
            self.anim_radius_start = self.radius
            self.anim_radius_target = up_target

        def handle_enter():

            self.basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.basic_tween.start()
            self.basic_tween.update()
            self.anim_radius_start = self.radius
            self.anim_radius_target = enter_target

        def handle_leave():

            self.basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.basic_tween.start()
            self.basic_tween.update()
            self.anim_radius_start = self.radius
            self.anim_radius_target = rest_target

        self.button.on(ButtonEvents.CLICK, handle_click)
        self.button.on(ButtonEvents.DOWN, handle_down)
        self.button.on(ButtonEvents.UP, handle_up)
        self.button.on(ButtonEvents.ENTER, handle_enter)
        self.button.on(ButtonEvents.LEAVE, handle_leave)

    def start(self):
        self.start_time = get_ticks()

    def render(self, delta_time: float, time: float):
        if self.value is None:
            rect(
                self.screen,
                Color(230, 230, 230),
                Rect(
                    self.x - self.radius,
                    self.y - self.radius,
                    2 * self.radius,
                    2 * self.radius,
                ),
                width=2,
                border_radius=20,
            )

            return

        rect(
            self.screen,
            Color(230, 230, 230),
            Rect(
                self.x - self.radius,
                self.y - self.radius,
                2 * self.radius,
                2 * self.radius,
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
            min(
                255,
                int(round(self.anim_radius.value / max(self.radius, 0.01) * 255, 0)),
            )
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
            self.radius = self.anim_radius.value

        if self.basic_tween.animating:
            self.basic_tween.update()
            self.radius = self.anim_radius_start + self.basic_tween.value * (
                self.anim_radius_target - self.anim_radius_start
            )

        self.button.rect = Rect(
            self.x - self.anim_radius.value,
            self.y - self.anim_radius.value,
            2 * self.anim_radius.value,
            2 * self.anim_radius.value,
        )

        self.button.update(delta_time, time)
