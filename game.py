import pygame
import random

# Định nghĩa kích thước cửa sổ trò chơi
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Định nghĩa kích thước của mỗi ô trên bảng
CELL_SIZE = 80

# Định nghĩa các màu sắc
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ trò chơi
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pipes Puzzle")

clock = pygame.time.Clock()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice(["horizontal", "vertical"])

        # Vẽ ống
        pygame.draw.rect(self.image, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))
        if self.direction == "horizontal":
            pygame.draw.line(self.image, BLUE, (0, CELL_SIZE // 2), (CELL_SIZE, CELL_SIZE // 2), 6)
        else:
            pygame.draw.line(self.image, BLUE, (CELL_SIZE // 2, 0), (CELL_SIZE // 2, CELL_SIZE), 6)

    def rotate(self):
        # Xoay ống
        if self.direction == "horizontal":
            self.direction = "vertical"
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))
            pygame.draw.line(self.image, BLUE, (CELL_SIZE // 2, 0), (CELL_SIZE // 2, CELL_SIZE), 6)
        else:
            self.direction = "horizontal"
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))
            pygame.draw.line(self.image, BLUE, (0, CELL_SIZE // 2), (CELL_SIZE, CELL_SIZE // 2), 6)

# Khởi tạo bảng trống
board = [[None] * (SCREEN_WIDTH // CELL_SIZE) for _ in range(SCREEN_HEIGHT // CELL_SIZE)]

# Đặt ô nguồn nước
source_x = random.randint(0, len(board[0]) - 1)
source_y = random.randint(0, len(board) - 1)
board[source_y][source_x] = Pipe(source_x * CELL_SIZE, source_y * CELL_SIZE)

# Đặt ống ngẫu nhiên trên bảng
for y in range(len(board)):
    for x in range(len(board[y])):
        if board[y][x] is None:
            board[y][x] = Pipe(x * CELL_SIZE, y * CELL_SIZE)

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra khi người chơi nhấp chuột
            if event.button == 1:  # Chuột trái - Di chuyển ống
                x, y = event.pos
                cell_x = x // CELL_SIZE
                cell_y = y // CELL_SIZE
                if isinstance(board[cell_y][cell_x], Pipe):
                    selected_pipe = board[cell_y][cell_x]
            elif event.button == 3:  # Chuột phải - Xoay ống
                x, y = event.pos
                cell_x = x // CELL_SIZE
                cell_y = y // CELL_SIZE
                if isinstance(board[cell_y][cell_x], Pipe):
                    board[cell_y][cell_x].rotate()

        elif event.type == pygame.MOUSEBUTTONUP:
            # Khi người chơi nhả chuộttrò chơi sẽ không được hoàn thiện vì hạn chế không thể thực hiện các hành động như "di chuyển" và "xoay" trong trò chơi Pipes Puzzle. Tuy nhiên, tôi đã cung cấp một mẫu mã đơn giản để bạn có thể bắt đầu xây dựng trò chơi Pipes Puzzle sử dụng thư viện Pygame. Bạn có thể tiếp tục phát triển mã này bằng cách thêm các chức năng và luật chơi phù hợp với trò chơi Pipes Puzzle.