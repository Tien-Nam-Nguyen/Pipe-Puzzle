from pygame.rect import Rect
from tweener import Tween, Easing, EasingMode

from .Button import Button, ButtonEvents


class ScaleButton(Button):
    def __init__(self, rect: Rect, hover_scale=1.2, pressed_scale=1.3):
        super().__init__(rect)
        rest_scale = 1.0

        self.__original_rect = rect.copy()
        self.__scaled_rect = rect.copy()

        self.__current_scale = rest_scale
        self.__start_scale = rest_scale
        self.__end_scale = rest_scale

        self.__basic_tween = None

        def handle_down():
            self.__basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.__basic_tween.start()
            self.__basic_tween.update()
            self.__start_scale = self.__current_scale
            self.__end_scale = pressed_scale

        def handle_up():
            self.__basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.__basic_tween.start()
            self.__basic_tween.update()
            self.__start_scale = self.__current_scale
            self.__end_scale = rest_scale

        def handle_enter():
            self.__basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.__basic_tween.start()
            self.__basic_tween.update()
            self.__start_scale = self.__current_scale
            self.__end_scale = hover_scale

        def handle_leave():
            self.__basic_tween = Tween(0.0, 1.0, 500, Easing.ELASTIC, EasingMode.OUT)
            self.__basic_tween.start()
            self.__basic_tween.update()
            self.__start_scale = self.__current_scale
            self.__end_scale = rest_scale

        self.on(ButtonEvents.DOWN, handle_down)
        self.on(ButtonEvents.UP, handle_up)
        self.on(ButtonEvents.ENTER, handle_enter)
        self.on(ButtonEvents.LEAVE, handle_leave)

    @property
    def original_rect(self) -> Rect:
        return self.__original_rect

    @property
    def scaled_rect(self) -> Rect:
        return self.__scaled_rect

    def set_original_rect(self, x: float, y: float, width: float, height: float):
        self.__original_rect.update(x, y, width, height)

    def update(self, delta_time: float, time: float):
        super().update(delta_time, time)

        if self.__basic_tween is None:
            return

        self.__basic_tween.update()
        self.__current_scale = (
            self.__basic_tween.value * self.__end_scale
            + (1 - self.__basic_tween.value) * self.__start_scale
        )

        self.__scaled_rect.update(
            self.__original_rect.x
            - (
                self.__original_rect.width * self.__current_scale
                - self.__original_rect.width
            )
            / 2,
            self.__original_rect.y
            - (
                self.__original_rect.height * self.__current_scale
                - self.__original_rect.height
            )
            / 2,
            self.__original_rect.width * self.__current_scale,
            self.__original_rect.height * self.__current_scale,
        )
