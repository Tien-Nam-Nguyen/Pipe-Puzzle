import pygame

from .Anchor import Anchor
from .Bridge import Bridge
from ..utils import create_game, reset, copy_connections
from ..GameState import Bounds, GameState, Coordinate


def gui():
    if not pygame.font:
        raise ImportError("pygame.font not available")

    if not pygame.mixer:
        raise ImportError("pygame.mixer not available")

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    ncols = 7
    nrows = 7

    bounds = Bounds(ncols - 1, nrows - 1, 0, 0)
    anchor_count = 7
    first_state = create_game(anchor_count, bounds, 1)
    # first_state = reset(solution)

    board_size = 500

    bridges = convert_to_bridges(screen, clock, bounds, first_state, board_size)
    anchors = convert_to_anchors(screen, clock, bounds, first_state, board_size)

    game_objects = [*bridges, *anchors]

    delta_time = 0
    time = 0

    for game_object in game_objects:
        game_object.start()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        for game_object in game_objects:
            game_object.render(delta_time, time)

        for game_object in game_objects:
            game_object.update(delta_time, time)

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000  # limits FPS to 60
        time = pygame.time.get_ticks()

    pygame.quit()


def convert_to_anchors(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    bounds: Bounds,
    game_state: GameState,
    board_size: float,
):
    min_size = max(bounds.right, bounds.top, 1)
    anchor_size = board_size / min_size
    anchor_radius = anchor_size * 0.4

    anchors: list[Anchor] = []
    for y in range(0, bounds.top + 1):
        for x in range(0, bounds.right + 1):
            entry = next(
                (
                    (a, conn)
                    for a, conn in game_state.connections.items()
                    if a.x == x and a.y == y
                ),
                None,
            )

            if entry is None:
                anchors.append(
                    Anchor(
                        screen,
                        clock,
                        (screen.get_width() - board_size) // 2 + anchor_size * x,
                        (screen.get_height() - board_size) // 2 + anchor_size * y,
                        anchor_radius,
                        100 * (x + y),
                    )
                )
                continue

            _, connection = entry

            anchors.append(
                Anchor(
                    screen,
                    clock,
                    (screen.get_width() - board_size) // 2 + anchor_size * x,
                    (screen.get_height() - board_size) // 2 + anchor_size * y,
                    anchor_radius,
                    100 * (x + y),
                    connection.max_count,
                )
            )

    return anchors


def convert_to_bridges(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    bounds: Bounds,
    game_state: GameState,
    board_size: float,
):
    min_size = max(bounds.right, bounds.top, 1)
    anchor_size = board_size / min_size

    copy = copy_connections(game_state.connections)

    bridges: list[tuple[Coordinate, Coordinate, bool]] = []
    for coord, connection in copy.items():
        for target in set(connection.connected):
            appearance = connection.connected.count(target)

            if appearance > 1:
                bridges.append((coord, target, True))
            else:
                bridges.append((coord, target, False))

            while coord in copy[target].connected:
                copy[target].connected.remove(coord)

    bridge_objects = [
        Bridge(
            screen,
            clock,
            (
                (screen.get_width() - board_size) // 2 + anchor_size * (coord.x),
                (screen.get_height() - board_size) // 2 + anchor_size * (coord.y),
            ),
            (
                (screen.get_width() - board_size) // 2 + anchor_size * (target.x),
                (screen.get_height() - board_size) // 2 + anchor_size * (target.y),
            ),
            500,
            is_double,
        )
        for coord, target, is_double in bridges
    ]

    return bridge_objects
