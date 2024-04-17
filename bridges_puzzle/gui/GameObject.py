from pygame.time import Clock
from pygame.surface import Surface


class GameObject:
    __screen: Surface | None
    __clock: Clock | None

    def __init__(self) -> None:
        self.__active = True

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        if self.__active == False and value == True:
            self.__active = True
            self.start()

        self.__active = value

    @staticmethod
    def init(screen: Surface, clock: Clock):
        GameObject.__screen = screen
        GameObject.__clock = clock

    @property
    def screen(self) -> Surface:
        if GameObject.__screen is None:
            raise Exception("GameObject has not been initialized")

        return GameObject.__screen

    @property
    def clock(self) -> Clock:
        if GameObject.__clock is None:
            raise Exception("GameObject has not been initialized")

        return GameObject.__clock

    def engine_start(self):
        if self.active:
            self.start()

    def engine_render(self, delta_time: float, time: float):
        if self.active:
            self.render(delta_time, time)

    def engine_update(self, delta_time: float, time: float):
        if self.active:
            self.update(delta_time, time)

    def start(self):
        # OVERRIDE THIS METHOD
        pass

    def render(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass

    def update(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass
