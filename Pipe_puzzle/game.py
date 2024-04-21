import pygame
from copy import deepcopy
import time
from core import get_tile_index, blind_search
from game_utils import create_grid, update_grid, copy_grid

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Kích thước grid
DEFAULT_GRID_SIZE = 4
GRID_SIZE_3x3 = 3
GRID_SIZE_4x4 = 4
GRID_SIZE_5x5 = 5
CELL_SIZE = 100
CELL_PADDING = 10

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)



# Khởi tạo cửa sổ game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Game")

clock = pygame.time.Clock()

# Hàm tạo grid với các bức ảnh từ thư mục



# Hàm lấy danh sách đường dẫn đến các ảnh trong thư mục
# Hàm vẽ grid lên màn hình
def draw_grid(grid):
    screen.fill(WHITE)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x = j * (CELL_SIZE + CELL_PADDING)
            y = i * (CELL_SIZE + CELL_PADDING)

            # Vẽ biên giới của ô
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

            # Vẽ bức ảnh tại vị trí ô trong grid
            screen.blit(grid[i][j], (x + CELL_PADDING // 2, y + CELL_PADDING // 2))

    # pygame.display.flip()

def draw_3x3_new_game_button():
    font = pygame.font.SysFont('Georgia', 18, bold=True)

    # Vẽ nút "New Game 3x3"
    button_3x3 = pygame.Rect(SCREEN_WIDTH - 220, 50, 160, 30)
    pygame.draw.rect(screen, BLUE, button_3x3)
    text_3x3 = font.render("New Game 3x3", True, WHITE)
    screen.blit(text_3x3, (button_3x3.x + 10, button_3x3.y + 5))

    return button_3x3



# Hàm vẽ các nút "New Game"
def draw_new_game_buttons():
    font = pygame.font.SysFont('Georgia', 18, bold=True)
    
    # Vẽ nút "New Game 4x4"
    button_4x4 = pygame.Rect(SCREEN_WIDTH - 220, 110, 160, 30)
    pygame.draw.rect(screen, BLUE, button_4x4)
    text_4x4 = font.render("New Game 4x4", True, WHITE)
    screen.blit(text_4x4, (button_4x4.x + 10, button_4x4.y + 5))

    # Vẽ nút "New Game 5x5"
    button_5x5 = pygame.Rect(SCREEN_WIDTH - 220, 170, 160, 30)
    pygame.draw.rect(screen, BLUE, button_5x5)
    text_5x5 = font.render("New Game 5x5", True, WHITE)
    screen.blit(text_5x5, (button_5x5.x + 10, button_5x5.y + 5))

    return button_4x4, button_5x5


def draw_a_star_solve_button():
    font = pygame.font.SysFont('Georgia', 18, bold=True)
    button_solve = pygame.Rect(SCREEN_WIDTH - 220, 230, 160, 30)
    pygame.draw.rect(screen, GREEN, button_solve)
    text_solve = font.render("A* Solve", True, WHITE)
    screen.blit(text_solve, (button_solve.x + 10, button_solve.y + 5))
    return button_solve


def draw_dfs_solve_button():
    font = pygame.font.SysFont('Georgia', 18, bold=True)
    button_solve = pygame.Rect(SCREEN_WIDTH - 220, 290, 160, 30)
    pygame.draw.rect(screen, GREEN, button_solve)
    text_solve = font.render("DFS Solve", True, WHITE)
    screen.blit(text_solve, (button_solve.x + 10, button_solve.y + 5))
    return button_solve


def draw_dfs_reset_state_3x3():
    font = pygame.font.SysFont('Georgia', 18, bold=True)
    button_solve = pygame.Rect(SCREEN_WIDTH - 200, 350, 135, 30)
    pygame.draw.rect(screen, GREEN, button_solve)
    text_solve = font.render("RESET 3x3", True, WHITE)
    screen.blit(text_solve, (button_solve.x + 10, button_solve.y + 5))
    return button_solve


def draw_num_state(num_state=0):
    font = pygame.font.SysFont('Georgia', 22, bold=True)
    text = font.render(f'Number of stored states: {num_state}', True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH - 200, 430)
    screen.blit(text, text_rect)
    return text_rect


def draw_total_time(total_time=0):
    font = pygame.font.SysFont('Georgia', 22, bold=True)
    text = font.render(f'Total time: {round(total_time, 3)} seconds', True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH - 200, 530)
    screen.blit(text, text_rect)
    return text_rect


def draw_source(x, y):
    circle_radius = 22
    x = x * (CELL_SIZE + CELL_PADDING) + CELL_PADDING // 2 + CELL_SIZE // 2
    y = y * (CELL_SIZE + CELL_PADDING) + CELL_PADDING // 2 + CELL_SIZE // 2
    circle_center = (y, x)
    pygame.draw.circle(screen, RED, circle_center, circle_radius)


# Hàm chính
def main():
    solved = False
    rotate_solving_event = pygame.USEREVENT + 1
    pygame.time.set_timer(rotate_solving_event, 1000)
    grid_size = DEFAULT_GRID_SIZE
    grid, instructions, num_state, total_time, all_tiles, image_dict = create_grid(grid_size)
    a_star_instructions_3x3 = None
    a_star_grid_3x3 = None
    a_star_num_state_3x3 = None
    a_star_total_time = None
    a_star_all_tiles = None
    src = all_tiles[0]
    print(f'source : {src.x} {src.y}')

    instruction_x, instruction_y, instruction_cmd = None, None, None
    instructions_idx = 0
    solving = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if solving and event.type == rotate_solving_event:
                idx = get_tile_index(instruction_x, instruction_y, all_tiles)
                if instruction_cmd == 'left':
                    # actually rotate in logic and update visually tile by tile
                    all_tiles[idx].rotate_left(src, all_tiles)
                    grid, all_tiles = update_grid(grid, image_dict, all_tiles)
                
                elif instruction_cmd == 'right':
                    all_tiles[idx].rotate_right(src, all_tiles)
                    grid, all_tiles = update_grid(grid, image_dict, all_tiles)

                else:
                    all_tiles[idx].rotate_left(src, all_tiles)
                    all_tiles[idx].rotate_left(src, all_tiles)
                    grid, all_tiles = update_grid(grid, image_dict, all_tiles)
                
                instructions_idx += 1
                if instructions_idx < len(instructions):
                    instruction_x, instruction_y, instruction_cmd = instructions[instructions_idx]
                else:
                    solving = False
                    solved = True
                    print('Finish solving')
                    instructions_idx = 0
                    pygame.time.set_timer(rotate_solving_event, 1000)
                    
                continue


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT or event.button == pygame.BUTTON_RIGHT:
                    # Tính toán vị trí ô trong grid dựa trên vị trí chuột
                    mouse_pos = pygame.mouse.get_pos()
                    grid_x = mouse_pos[0] // (CELL_SIZE + CELL_PADDING)
                    grid_y = mouse_pos[1] // (CELL_SIZE + CELL_PADDING)

                    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
                        # Xác định góc quay dựa trên nút chuột
                        rotation_angle = -90 if event.button == pygame.BUTTON_LEFT else 90

                        # Quay ô theo góc quay tương ứng
                        # grid[grid_y][grid_x] = pygame.transform.rotate(grid[grid_y][grid_x], rotation_angle)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    # Kiểm tra xem người chơi đã nhấp chuột vào nút "New Game 4x4"
                    if button_4x4.collidepoint(event.pos):
                        grid_size = GRID_SIZE_4x4
                        grid, instructions, num_state, total_time, all_tiles, image_dict = create_grid(grid_size)
                        src = all_tiles[0]
                        solved = False

                    # Kiểm tra xem người chơi đã nhấp chuột vào nút "New Game 5x5"
                    elif button_5x5.collidepoint(event.pos):
                        grid_size = GRID_SIZE_5x5
                        grid, instructions, num_state, total_time, all_tiles, image_dict = create_grid(grid_size)
                        src = all_tiles[0]
                        solved = False

                    elif button_3x3.collidepoint(event.pos):
                        grid_size = GRID_SIZE_3x3
                        grid, instructions, num_state, total_time, all_tiles, image_dict = create_grid(grid_size, mode='dfs')
                        a_star_instructions_3x3 = instructions.copy()
                        a_star_grid_3x3 = copy_grid(grid)
                        a_star_all_tiles = deepcopy(all_tiles)
                        a_star_num_state_3x3 = num_state
                        a_star_total_time = total_time
                        # a_star_all_tiles = deepcopy(all_tiles)
                        src = all_tiles[0]
                        solved = False

                    elif a_star_button_solve.collidepoint(event.pos):
                        solving = True
                        instruction_x, instruction_y, instruction_cmd = instructions[instructions_idx]
                        # instructions_idx += 1

                    elif dfs_button_solve.collidepoint(event.pos):
                        start_time = time.time() 
                        instructions, dfs_num_state = blind_search(all_tiles)
                        pygame.time.set_timer(rotate_solving_event, 100)
                        print(f'Dfs: {len(instructions)}')
                        num_state = dfs_num_state
                        total_time = time.time() - start_time 
                        solved = True
                        solving = True
                        instructions_idx = 0
                        instruction_x, instruction_y, instruction_cmd = instructions[instructions_idx]

                    elif reset_3x3_btn.collidepoint(event.pos):
                        print('wtf')
                        grid = copy_grid(a_star_grid_3x3)
                        all_tiles = deepcopy(a_star_all_tiles)
                        total_time = a_star_total_time
                        instructions = a_star_instructions_3x3
                        num_state = a_star_num_state_3x3
                        solved = False


        draw_grid(grid)
        button_3x3 = draw_3x3_new_game_button()
        button_4x4, button_5x5 = draw_new_game_buttons()
        
        if not solved:
            a_star_button_solve = draw_a_star_solve_button()

        if grid_size == GRID_SIZE_3x3 and not solved:
            dfs_button_solve = draw_dfs_solve_button()

        if grid_size == GRID_SIZE_3x3 and solved:    
            reset_3x3_btn = draw_dfs_reset_state_3x3()

        num_state_rect = draw_num_state(num_state)
        total_time_rect = draw_total_time(total_time)
        draw_source(src.x, src.y)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()