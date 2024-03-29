import pygame
import os
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Kích thước grid
DEFAULT_GRID_SIZE = 5
GRID_SIZE_4x4 = 4
GRID_SIZE_5x5 = 5
CELL_SIZE = 100
CELL_PADDING = 10

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Đường dẫn đến thư mục chứa ảnh
IMAGE_FOLDER = "images"

# Khởi tạo cửa sổ game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Game")

clock = pygame.time.Clock()

# Hàm tạo grid với các bức ảnh từ thư mục
def create_grid(grid_size):
    grid = []
    image_paths = get_image_paths()
    for _ in range(grid_size):
        row = []
        for _ in range(grid_size):
            # Chọn một bức ảnh ngẫu nhiên từ thư mục
            image_path = random.choice(image_paths)
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
            row.append(image)
        grid.append(row)
    return grid

# Hàm lấy danh sách đường dẫn đến các ảnh trong thư mục
def get_image_paths():
    image_paths = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(IMAGE_FOLDER, filename)
            image_paths.append(image_path)
    return image_paths

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

# Hàm vẽ các nút "New Game"
def draw_new_game_buttons():
    font = pygame.font.SysFont('Georgia', 18, bold=True)

    # Vẽ nút "New Game 4x4"
    button_4x4 = pygame.Rect(SCREEN_WIDTH - 200, 50, 135, 30)
    pygame.draw.rect(screen, BLUE, button_4x4)
    text_4x4 = font.render("New Game 4x4", True, WHITE)
    screen.blit(text_4x4, (button_4x4.x + 10, button_4x4.y + 5))

    # Vẽ nút "New Game 5x5"
    button_5x5 = pygame.Rect(SCREEN_WIDTH - 200, 110, 135, 30)
    pygame.draw.rect(screen, BLUE, button_5x5)
    text_5x5 = font.render("New Game 5x5", True, WHITE)
    screen.blit(text_5x5, (button_5x5.x + 10, button_5x5.y + 5))

    return button_4x4, button_5x5


def draw_solve_button():
    font = pygame.font.SysFont('Georgia', 18, bold=True)
    button_solve = pygame.Rect(SCREEN_WIDTH - 200, 170, 135, 30)
    pygame.draw.rect(screen, GREEN, button_solve)
    text_solve = font.render("Solve", True, WHITE)
    screen.blit(text_solve, (button_solve.x + 10, button_solve.y + 5))
    return button_solve


# Hàm chính
def main():
    grid_size = DEFAULT_GRID_SIZE
    grid = create_grid(grid_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                        grid[grid_y][grid_x] = pygame.transform.rotate(grid[grid_y][grid_x], rotation_angle)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    # Kiểm tra xem người chơi đã nhấp chuột vào nút "New Game 4x4"
                    if button_4x4.collidepoint(event.pos):
                        grid_size = GRID_SIZE_4x4
                        grid = create_grid(grid_size)
                    # Kiểm tra xem người chơi đã nhấp chuột vào nút "New Game 5x5"
                    elif button_5x5.collidepoint(event.pos):
                        grid_size = GRID_SIZE_5x5
                        grid = create_grid(grid_size)
                    
                    elif button_solve.collidepoint(event.pos):
                        print('Solve button is clicked')

        draw_grid(grid)
        button_4x4, button_5x5 = draw_new_game_buttons()
        button_solve = draw_solve_button()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()