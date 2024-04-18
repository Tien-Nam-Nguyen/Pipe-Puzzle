import pygame
from typing import NamedTuple, Callable
from enum import Enum
from random import seed, randint

from .Anchor import Anchor, DEFAULT_COLOR
from .Bridge import Bridge
from .Wire import Wire
from .Button import Button, ButtonEvents
from .ScaleButton import ScaleButton
from .LabelButton import LabelButton
from .QuadraticBezier import QuadraticBezier
from .GameObject import GameObject
from ..utils import create_game, reset, copy_connections, connect, dfs, a_star
from ..GameState import Bounds, GameState, Coordinate, Connection

GAME_OBJECTS: list[GameObject] = [
    Button,
    ScaleButton,
    LabelButton,
    Anchor,
    Bridge,
    Wire,
    QuadraticBezier,
]

SCREEN_SIZE = (1280, 720)
BOARD_SIZE = 600


class GameDifficulty(Enum):
    EASY = 0
    MEDIUM = 5
    HARD = 9


class BoardSize(Enum):
    SMALL = 7
    MEDIUM = 10
    LARGE = 15


def generate_anchor_count(
    difficulty: GameDifficulty,
    seed_value: int | float | str | bytes | bytearray | None = None,
):
    seed(seed_value)

    match difficulty:
        case GameDifficulty.EASY:
            return randint(4, 8)
        case GameDifficulty.MEDIUM:
            return randint(9, 15)
        case GameDifficulty.HARD:
            return randint(16, 20)

    return 4


def generate_base_game(
    difficulty: GameDifficulty,
    size: BoardSize,
    seed_value: int | float | str | bytes | bytearray | None = None,
) -> tuple[GameState, GameState, Bounds, int]:
    bounds = Bounds(size.value - 1, size.value - 1, 0, 0)
    anchor_count = generate_anchor_count(difficulty, seed_value)
    solution = create_game(anchor_count, bounds, difficulty.value, seed_value)
    game_state = reset(solution)

    return game_state, solution, bounds, anchor_count


def generate_game_objects(game_state: GameState):
    bridges = convert_to_bridges(game_state)
    anchors = convert_to_anchors(game_state)
    return bridges, anchors


def init():
    if not pygame.font:
        raise ImportError("pygame.font not available")

    if not pygame.mixer:
        raise ImportError("pygame.mixer not available")

    pygame.init()
    pygame.display.set_caption("Bridges Puzzle")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    for obj in GAME_OBJECTS:
        obj.init(screen, clock)

    return screen, clock


def gui(
    difficulty: GameDifficulty = GameDifficulty.EASY, size: BoardSize = BoardSize.SMALL
):
    screen, clock = init()

    start_state, _solution, _bounds, _anchor_count = generate_base_game(
        difficulty, size
    )

    game_state = start_state

    bridges, anchors = generate_game_objects(game_state)

    def update_bridges_objects(bridges: list[Bridge]):
        nonlocal game_objects
        nonlocal static_objects

        game_objects = [*bridges, *static_objects]
        for bridge in bridges:
            bridge.start()

    def get_game_state():
        return game_state

    def set_game_state(new_game_state: GameState):
        nonlocal game_state
        game_state = new_game_state

    def get_input_mode():
        return input_mode_data.input_mode

    wire = create_selector(
        anchors,
        get_game_state,
        get_input_mode,
        update_bridges_objects,
        set_game_state,
    )

    input_mode_data, dfs_button, a_star_button = create_ui(
        anchors,
        get_game_state,
        update_bridges_objects,
        set_game_state,
    )

    static_objects: list[GameObject] = [
        wire,
        *(anchors.values()),
        input_mode_data.button,
        dfs_button,
        a_star_button,
    ]

    game_objects: list[GameObject] = [*bridges, *static_objects]

    delta_time = 0
    time = 0

    for game_object in game_objects:
        game_object.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        for game_object in game_objects:
            game_object.engine_update(delta_time, time)

        for game_object in game_objects:
            game_object.engine_render(delta_time, time)

        pygame.display.flip()

        delta_time = clock.tick(60) / 1000
        time = pygame.time.get_ticks()

    pygame.quit()


def convert_to_anchors(
    game_state: GameState,
):
    connections, bounds = game_state
    min_size = max(bounds.right, bounds.top, 1)
    anchor_size = BOARD_SIZE / (min_size + 1)
    anchor_radius = anchor_size * 0.4

    anchors: dict[Coordinate, Anchor] = {}
    for y in range(0, bounds.top + 1):
        for x in range(0, bounds.right + 1):
            entry = next(
                ((a, conn) for a, conn in connections.items() if a.x == x and a.y == y),
                None,
            )

            if entry is None:
                anchors[Coordinate(x, y)] = Anchor(
                    (SCREEN_SIZE[0] - BOARD_SIZE) // 2
                    + anchor_size * x
                    + anchor_size // 2,
                    (SCREEN_SIZE[1] - BOARD_SIZE) // 2
                    + anchor_size * y
                    + anchor_size // 2,
                    anchor_radius,
                    100 * (x + y),
                )
                continue

            _, connection = entry

            anchors[Coordinate(x, y)] = Anchor(
                (SCREEN_SIZE[0] - BOARD_SIZE) // 2 + anchor_size * x + anchor_size // 2,
                (SCREEN_SIZE[1] - BOARD_SIZE) // 2 + anchor_size * y + anchor_size // 2,
                anchor_radius,
                100 * (x + y),
                connection.max_count - len(connection.connected),
            )

    return anchors


def convert_to_bridges(
    game_state: GameState,
):
    connections, bounds = game_state
    min_size = max(bounds.right, bounds.top, 1)
    anchor_size = BOARD_SIZE / (min_size + 1)

    copy = copy_connections(connections)

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
                (SCREEN_SIZE[0] - BOARD_SIZE) // 2
                + anchor_size * (coord.x)
                + anchor_size // 2,
                (SCREEN_SIZE[1] - BOARD_SIZE) // 2
                + anchor_size * (coord.y)
                + anchor_size // 2,
            ),
            (
                (SCREEN_SIZE[0] - BOARD_SIZE) // 2
                + anchor_size * (target.x)
                + anchor_size // 2,
                (SCREEN_SIZE[1] - BOARD_SIZE) // 2
                + anchor_size * (target.y)
                + anchor_size // 2,
            ),
            is_double,
        )
        for coord, target, is_double in bridges
    ]

    return bridge_objects


class InputType(Enum):
    ADD = 0
    REMOVE = 1


def get_input_label(type: InputType):
    match type:
        case InputType.ADD:
            return "Add"
        case InputType.REMOVE:
            return "Remove"

    return "Unknown"


def get_input_color(type: InputType):
    match type:
        case InputType.ADD:
            return pygame.Color(200, 240, 200)
        case InputType.REMOVE:
            return pygame.Color(240, 200, 200)

    return pygame.Color(200, 200, 200)


class SelectedAnchor(NamedTuple):
    anchor: Anchor
    coords: Coordinate


SELECTED_COLOR = pygame.Color(190, 190, 190)


def create_selector(
    anchors: dict[Coordinate, Anchor],
    get_game_state: Callable[[], GameState],
    get_selection_mode: Callable[[], InputType],
    update_bridges_objects: Callable[[list[Bridge]], None],
    set_game_state: Callable[[GameState], None],
):
    non_none_anchors = {
        coords: anchor for coords, anchor in anchors.items() if anchor.value is not None
    }
    wire = Wire(0, 0, BOARD_SIZE)
    wire.active = False

    selected: SelectedAnchor | None = None

    def enable_wire(anchor: Anchor):
        wire.active = True
        wire.x = anchor.x
        wire.y = anchor.y

    def disable_wire():
        wire.active = False

    def select(anchor: Anchor, coords: Coordinate):
        nonlocal selected

        if selected and selected.anchor is anchor:
            selected.anchor.color = DEFAULT_COLOR
            selected = None
            wire.active = False
            return

        if not selected:
            selected = SelectedAnchor(anchor, coords)
            selected.anchor.color = SELECTED_COLOR
            enable_wire(anchor)
            return

        try:
            game_state = get_game_state()
            connections = connect(game_state.connections, selected.coords, coords)
            new_game_state = GameState(connections, game_state.bounds)

            bridges = convert_to_bridges(new_game_state)
            anchor.value = calc_anchor_value(coords, new_game_state.connections)
            selected.anchor.value = calc_anchor_value(
                selected.coords, new_game_state.connections
            )

            set_game_state(new_game_state)
            update_bridges_objects(bridges)

            selected.anchor.color = DEFAULT_COLOR
            selected = None
            disable_wire()
        except Exception as e:
            print(e)

    def remove_attached_connections(anchor: Anchor, coords: Coordinate):
        game_state = get_game_state()
        connections = copy_connections(game_state.connections)

        for coords_to_remove in connections[coords].connected:
            connections[coords_to_remove].connected.remove(coords)
            restored = calc_anchor_value(coords_to_remove, connections)
            anchors[coords_to_remove].value = restored

        connections[coords].connected.clear()

        new_game_state = GameState(connections, game_state.bounds)

        bridges = convert_to_bridges(new_game_state)

        set_game_state(new_game_state)
        update_bridges_objects(bridges)

        anchor.value = new_game_state.connections[coords].max_count

    def handle_click_anchor(anchor: Anchor, coords: Coordinate):
        selection_mode = get_selection_mode()
        if selection_mode == InputType.ADD:
            select(anchor, coords)
        elif selection_mode == InputType.REMOVE:
            remove_attached_connections(anchor, coords)
        else:
            raise ValueError(f"Unimplemented selection mode: {selection_mode}")

    for coords, anchor in non_none_anchors.items():
        anchor.button.on(
            ButtonEvents.CLICK,
            lambda anchor=anchor, coords=coords: handle_click_anchor(anchor, coords),
        )

    return wire


INPUT_MODE_BUTTON_POSITION = (100, 60)


def create_ui(
    anchors: dict[Coordinate, Anchor],
    get_game_state: Callable[[], GameState],
    update_bridges_objects: Callable[[list[Bridge]], None],
    set_game_state: Callable[[GameState], None],
):
    input_mode_options = create_input_mode_button()

    dfs_solve = create_dfs_solver()
    a_star_solve = create_a_star_solver()

    dfs_solve_button = create_solver_button(
        100,
        140,
        "DFS",
        pygame.Color(240, 240, 160),
        dfs_solve,
        anchors,
        get_game_state,
        set_game_state,
        update_bridges_objects,
    )

    a_star_solve_button = create_solver_button(
        100,
        220,
        "A*",
        pygame.Color(200, 200, 250),
        a_star_solve,
        anchors,
        get_game_state,
        set_game_state,
        update_bridges_objects,
    )

    return input_mode_options, dfs_solve_button, a_star_solve_button


class InputModeButton:
    def __init__(self, input_mode: InputType, input_mode_button: LabelButton) -> None:
        self.input_mode = input_mode
        self.button = input_mode_button


def create_input_mode_button():
    init_input_mode = InputType.ADD

    data = InputModeButton(
        init_input_mode,
        LabelButton(
            INPUT_MODE_BUTTON_POSITION[0],
            INPUT_MODE_BUTTON_POSITION[1],
            get_input_label(init_input_mode),
            get_input_color(init_input_mode),
        ),
    )

    def toggle_input_type():
        data.input_mode = (
            InputType.ADD if data.input_mode == InputType.REMOVE else InputType.REMOVE
        )

        color = get_input_color(data.input_mode)
        label = get_input_label(data.input_mode)

        data.button.label = label
        data.button.color = color

    data.button.button.on(ButtonEvents.CLICK, toggle_input_type)

    return data


def calc_anchor_value(coords: Coordinate, connections: dict[Coordinate, Connection]):
    return connections[coords].max_count - len(connections[coords].connected)


def create_dfs_solver():
    cache: dict[GameState, tuple[Coordinate, Coordinate]] = {}

    def dfs_solve(game_state: GameState):
        if game_state in cache:
            return cache[game_state]

        try:
            solution = dfs(game_state)

            curr_state = game_state
            for next_state, move in zip(solution.states, solution.moves):
                cache[curr_state] = move
                curr_state = next_state

            # Solved state
            cache[solution.states[-1]] = None

            return cache[game_state]
        except Exception as e:
            print(e)
            return None

    return dfs_solve


def create_a_star_solver():
    cache: dict[GameState, tuple[Coordinate, Coordinate]] = {}

    def a_star_solve(game_state: GameState):
        if game_state in cache:
            return cache[game_state]

        try:
            solution = a_star(game_state)

            prev_state = game_state
            for state, move in zip(solution.states, solution.moves):
                cache[prev_state] = move
                prev_state = state

            return cache[game_state]
        except Exception as e:
            print(e)
            return None

    return a_star_solve


def create_solver_button(
    x: float,
    y: float,
    label: str,
    color: pygame.Color,
    solve: Callable[[GameState], tuple[Coordinate, Coordinate] | None],
    anchors: dict[Coordinate, Anchor],
    get_game_state: Callable[[], GameState],
    set_game_state: Callable[[GameState], None],
    update_bridges_objects: Callable[[list[Bridge]], None],
):
    def solve_dfs():
        game_state = get_game_state()
        move = solve(game_state)

        if move is None:
            return

        connections = connect(game_state.connections, move[0], move[1])
        new_game_state = GameState(connections, game_state.bounds)

        bridges = convert_to_bridges(new_game_state)
        anchors[move[0]].value = calc_anchor_value(move[0], new_game_state.connections)
        anchors[move[1]].value = calc_anchor_value(move[1], new_game_state.connections)

        set_game_state(new_game_state)
        update_bridges_objects(bridges)

    button = LabelButton(x, y, label, color)
    button.button.on(ButtonEvents.CLICK, solve_dfs)
    return button


def create_reset_button():
    pass
