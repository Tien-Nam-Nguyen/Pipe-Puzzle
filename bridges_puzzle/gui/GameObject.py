from pygame.time import Clock
from pygame.surface import Surface


class GameObject:
    _screen: Surface | None
    _clock: Clock | None

    @staticmethod
    def init(screen: Surface, clock: Clock):
        GameObject._screen = screen
        GameObject._clock = clock

    @property
    def screen(self) -> Surface:
        if GameObject._screen is None:
            raise Exception("GameObject has not been initialized")

        return GameObject._screen

    @property
    def clock(self) -> Clock:
        if GameObject._clock is None:
            raise Exception("GameObject has not been initialized")

        return GameObject._clock

    def start(self):
        # OVERRIDE THIS METHOD
        pass

    def render(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass

    def update(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass
