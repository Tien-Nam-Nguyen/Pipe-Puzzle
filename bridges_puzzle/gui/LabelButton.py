from pygame import font
from pygame.draw import rect
from pygame.color import Color
from pygame.rect import Rect

from .GameObject import GameObject
from .ScaleButton import ScaleButton


class LabelButton(GameObject):
    def __init__(
        self,
        x: float,
        y: float,
        label: str,
        color: Color = Color(230, 230, 230),
        padding=20,
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.__label = label
        self.color = color
        self.__padding = padding
        self.__font = font.Font(None, 36)
        self.__text = self.__font.render(label, True, "black")

        rect = self.__text.get_rect()
        self.button = ScaleButton(
            Rect(
                x - rect.width / 2 - padding,
                y - rect.height / 2 - padding,
                rect.width + 2 * padding,
                rect.height + 2 * padding,
            )
        )

        self.__rect = self.button.scaled_rect

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, value: str):
        self.__label = value
        self.__text = self.__font.render(value, True, "black")

        rect = self.__text.get_rect()
        self.button.set_original_rect(
            self.x - rect.width / 2 - self.__padding,
            self.y - rect.height / 2 - self.__padding,
            rect.width + 2 * self.__padding,
            rect.height + 2 * self.__padding,
        )

    def render(self, delta_time: float, time: float):
        rect(
            self.screen,
            self.color,
            self.__rect,
            border_radius=20,
        )

        self.screen.blit(
            self.__text,
            (
                self.x - self.__text.get_width() / 2,
                self.y - self.__text.get_height() / 2,
            ),
        )

    def update(self, delta_time: float, time: float):
        self.button.update(delta_time, time)

        rect = self.button.scaled_rect
        self.__rect.update(
            rect.x,
            rect.y,
            rect.width,
            rect.height,
        )
