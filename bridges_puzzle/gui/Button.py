from enum import Enum
from pygame.rect import Rect
from pygame.mouse import get_pos, get_pressed

from .GameObject import GameObject


class ButtonEvents(Enum):
    CLICK = "click"
    DOWN = "down"
    UP = "up"
    ENTER = "enter"
    LEAVE = "leave"


class Button(GameObject):
    def __init__(self, rect: Rect):
        self.rect = rect
        self._event_listener: dict[ButtonEvents, list[callable]] = {}

        self._clicked = False
        self._entered = False

    @property
    def clicked(self):
        return self._clicked

    @property
    def entered(self):
        return self._entered

    def on(self, event: ButtonEvents, callback: callable):
        if event not in self._event_listener:
            self._event_listener[event] = []

        self._event_listener[event].append(callback)

    def once(self, event: ButtonEvents, callback: callable):
        def once_callback(*args, **kwargs):
            callback(*args, **kwargs)
            self.off(event, once_callback)

        self.on(event, once_callback)

    def off(self, event: ButtonEvents, callback: callable):
        if event not in self._event_listener:
            return

        self._event_listener[event].remove(callback)

    def emit(self, event: ButtonEvents, *args, **kwargs):
        if event not in self._event_listener:
            return

        for callback in self._event_listener[event]:
            callback(*args, **kwargs)

    def update(self, delta_time: float, time: float):
        mouse_pos = get_pos()
        colliding = self.rect.collidepoint(mouse_pos)
        pressing = get_pressed()[0]

        if colliding and pressing and not self._clicked:
            self._clicked = True
            self.emit(ButtonEvents.DOWN)
            return

        if colliding and not pressing and self._clicked:
            self._clicked = False
            # self._entered = False
            self.emit(ButtonEvents.UP)
            self.emit(ButtonEvents.CLICK)
            return

        if not colliding and not pressing and self._clicked:
            self._clicked = False
            self.emit(ButtonEvents.UP)
            return

        if colliding and not self._entered:
            self._entered = True
            self.emit(ButtonEvents.ENTER)
            return

        if not colliding and self._entered:
            self._entered = False
            self.emit(ButtonEvents.LEAVE)
