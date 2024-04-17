import pygame
from typing import NamedTuple

from .Anchor import Anchor, DEFAULT_COLOR
from .Bridge import Bridge
from .Wire import Wire
from .Button import Button, ButtonEvents
from .QuadraticBezier import QuadraticBezier
from .GameObject import GameObject
from ..utils import create_game, reset, copy_connections, connect
from ..GameState import Bounds, GameState, Coordinate

SELECTED_COLOR = pygame.Color(190, 190, 190)


class SelectedAnchor(NamedTuple):
    anchor: Anchor
    coords: Coordinate


def gui():
    if not pygame.font:
        raise ImportError("pygame.font not available")

    if not pygame.mixer:
        raise ImportError("pygame.mixer not available")

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    OBJECTS: list[GameObject] = [
        Button,
        Anchor,
        Bridge,
        Wire,
        QuadraticBezier,
    ]

    for obj in OBJECTS:
        obj.init(screen, clock)

    running = True

    ncols = 7
    nrows = 7

    bounds = Bounds(ncols - 1, nrows - 1, 0, 0)
    anchor_count = 7
    game_state = create_game(anchor_count, bounds, 5, 0)
    game_state = reset(game_state)

    board_size = 500

    bridges = convert_to_bridges(screen, bounds, game_state, board_size)
    anchors = convert_to_anchors(screen, bounds, game_state, board_size)

    selected: SelectedAnchor | None = None
    wire = Wire(0, 0, board_size)
    wire.active = False

    static_objects: list[GameObject] = [wire, *(anchors.values())]
    game_objects: list[GameObject] = [*bridges, *static_objects]

    def select(anchor: Anchor, coords: Coordinate):
        nonlocal selected
        nonlocal game_objects
        nonlocal game_state

        if selected and selected.anchor is anchor:
            selected.anchor.color = DEFAULT_COLOR
            selected = None
            wire.active = False
            print(f"deselected {coords}")
            return

        if selected:
            try:
                connections = connect(game_state.connections, selected.coords, coords)
                game_state = GameState(connections, game_state.bounds)

                bridges = convert_to_bridges(screen, bounds, game_state, board_size)

                for bridge in bridges:
                    bridge.start()

                game_objects = [*bridges, *static_objects]

                anchor.value = game_state.connections[coords].max_count - len(
                    game_state.connections[coords].connected
                )

                selected.anchor.value = game_state.connections[
                    selected.coords
                ].max_count - len(game_state.connections[selected.coords].connected)

                selected.anchor.color = DEFAULT_COLOR
                selected = None
                wire.active = False
                return
            except Exception as e:
                print(e)
                return

        selected = SelectedAnchor(anchor, coords)
        selected.anchor.color = SELECTED_COLOR
        wire.active = True
        wire.x = anchor.x
        wire.y = anchor.y
        print(f"selected {coords}")

    for coords, anchor in anchors.items():
        if anchor.value is None:
            continue

        anchor.button.on(
            ButtonEvents.CLICK,
            lambda anchor=anchor, coords=coords: select(anchor, coords),
        )

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
            game_object.engine_update(delta_time, time)

        for game_object in game_objects:
            game_object.engine_render(delta_time, time)

        # flip() the display to put your work on screen
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000  # limits FPS to 60
        time = pygame.time.get_ticks()

    pygame.quit()


def convert_to_anchors(
    screen: pygame.Surface,
    bounds: Bounds,
    game_state: GameState,
    board_size: float,
):
    min_size = max(bounds.right, bounds.top, 1)
    anchor_size = board_size / min_size
    anchor_radius = anchor_size * 0.4

    anchors: dict[Coordinate, Anchor] = {}
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
                anchors[Coordinate(x, y)] = Anchor(
                    (screen.get_width() - board_size) // 2 + anchor_size * x,
                    (screen.get_height() - board_size) // 2 + anchor_size * y,
                    anchor_radius,
                    100 * (x + y),
                )
                continue

            _, connection = entry

            anchors[Coordinate(x, y)] = Anchor(
                (screen.get_width() - board_size) // 2 + anchor_size * x,
                (screen.get_height() - board_size) // 2 + anchor_size * y,
                anchor_radius,
                100 * (x + y),
                connection.max_count - len(connection.connected),
            )

    return anchors


def convert_to_bridges(
    screen: pygame.Surface,
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
            (
                (screen.get_width() - board_size) // 2 + anchor_size * (coord.x),
                (screen.get_height() - board_size) // 2 + anchor_size * (coord.y),
            ),
            (
                (screen.get_width() - board_size) // 2 + anchor_size * (target.x),
                (screen.get_height() - board_size) // 2 + anchor_size * (target.y),
            ),
            is_double,
        )
        for coord, target, is_double in bridges
    ]

    return bridge_objects
