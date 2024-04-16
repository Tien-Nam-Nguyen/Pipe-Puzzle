from pygame.time import Clock
from pygame.surface import Surface


class GameObject:
    def __init__(self, screen: Surface, clock: Clock):
        self.screen = screen
        self.clock = clock

    def start(self):
        # OVERRIDE THIS METHOD
        pass

    def render(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass

    def update(self, delta_time: float, time: float):
        # OVERRIDE THIS METHOD
        pass
