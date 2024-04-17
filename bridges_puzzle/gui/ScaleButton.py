from pygame.rect import Rect
from tweener import Tween, Easing, EasingMode

from .Button import Button, ButtonEvents


class ScaleButton(Button):
    def __init__(self, rect: Rect, hover_scale=1.2, pressed_scale=1.3):
        super().__init__(rect)
        rest_scale = 1.0

        self.original_rect = rect.copy()
        self.scaled_rect = rect.copy()

        self._current_scale = rest_scale
        self._start_scale = rest_scale
        self._end_scale = rest_scale

        self._basic_tween = None

        def handle_down():
            self._basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._basic_tween.start()
            self._basic_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = pressed_scale

        def handle_up():
            self._basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._basic_tween.start()
            self._basic_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = rest_scale

        def handle_enter():
            self._basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._basic_tween.start()
            self._basic_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = hover_scale

        def handle_leave():
            self._basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self._basic_tween.start()
            self._basic_tween.update()
            self._start_scale = self._current_scale
            self._end_scale = rest_scale

        self.on(ButtonEvents.DOWN, handle_down)
        self.on(ButtonEvents.UP, handle_up)
        self.on(ButtonEvents.ENTER, handle_enter)
        self.on(ButtonEvents.LEAVE, handle_leave)

    def update(self, delta_time: float, time: float):
        super().update(delta_time, time)

        if self._basic_tween is None:
            return

        self._basic_tween.update()
        self._current_scale = (
            self._basic_tween.value * self._end_scale
            + (1 - self._basic_tween.value) * self._start_scale
        )

        self.scaled_rect.update(
            self.original_rect.x
            - (
                self.original_rect.width * self._current_scale
                - self.original_rect.width
            )
            / 2,
            self.original_rect.y
            - (
                self.original_rect.height * self._current_scale
                - self.original_rect.height
            )
            / 2,
            self.original_rect.width * self._current_scale,
            self.original_rect.height * self._current_scale,
        )
