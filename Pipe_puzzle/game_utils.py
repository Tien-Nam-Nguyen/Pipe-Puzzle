import pygame
from core import init_and_get_solution
import os

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Đường dẫn đến thư mục chứa ảnh
CELL_SIZE = 100
IMAGE_FOLDER = "images"

def create_grid(grid_size, mode='a_star'):

    grid = []
    image_dict = get_image_dict()
    for _ in range(grid_size):
        row = []
        for _ in range(grid_size):
            # Chọn một bức ảnh ngẫu nhiên từ thư mục
            # image_path = random.choice(image_paths)
            # image = pygame.image.load(image_path)
            image = 1
            # image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
            row.append(image)
        grid.append(row)
    


    all_tiles, instructions, num_state, total_time = init_and_get_solution(grid_size, mode=mode)
    grid, all_tiles = update_grid(grid, image_dict, all_tiles)

        
    return grid, instructions, num_state, total_time, all_tiles, image_dict


def get_image_dict():
    image_paths = {}
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(IMAGE_FOLDER, filename)
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

            if filename.startswith('type1-water'):
                image_paths['right_water'] = image
            
            elif filename.startswith('type1'):
                image_paths['right'] = image

            elif filename.startswith('type2-water'):
                image_paths['left_right_water'] = image

            elif filename.startswith('type2'):
                image_paths['left_right'] = image

            elif filename.startswith('type3-water'):
                image_paths['down_right_water'] = image
            
            elif filename.startswith('type3'):
                image_paths['down_right'] = image

            elif filename.startswith('type4-water'):
                image_paths['up_down_right_water'] = image

            elif filename.startswith('type4'):
                image_paths['up_down_right'] = image

    # -90 theo chieu kim dong ho, 90 nguoc chieu kim dong ho
    CLOCKWISE, ANTI_CLOCKWISE = -90, 90

    right_water_base = image_paths['right_water']
    right_base = image_paths['right']
    left_right_water_base = image_paths['left_right_water']
    left_right_base = image_paths['left_right']
    down_right_water_base = image_paths['down_right_water']
    down_right_base = image_paths['down_right']
    up_down_right_water_base = image_paths['up_down_right_water']
    up_down_right_base = image_paths['up_down_right']


    # set deadend images
    image_paths['left_water'] = pygame.transform.rotate(right_water_base, 180)
    image_paths['left'] = pygame.transform.rotate(right_base, 180)
    image_paths['up_water'] = pygame.transform.rotate(right_water_base, ANTI_CLOCKWISE)
    image_paths['up'] = pygame.transform.rotate(right_base, ANTI_CLOCKWISE)
    image_paths['down_water'] = pygame.transform.rotate(right_water_base, CLOCKWISE)
    image_paths['down'] = pygame.transform.rotate(right_base, CLOCKWISE)

    # set straight pipe images
    image_paths['up_down_water'] = pygame.transform.rotate(left_right_water_base, CLOCKWISE)
    image_paths['up_down'] = pygame.transform.rotate(left_right_base, CLOCKWISE)

    # set L shape images
    image_paths['down_left_water'] = pygame.transform.rotate(down_right_water_base, CLOCKWISE)
    image_paths['down_left'] = pygame.transform.rotate(down_right_base, CLOCKWISE)
    image_paths['up_left_water'] = pygame.transform.rotate(down_right_water_base, 180)
    image_paths['up_left'] = pygame.transform.rotate(down_right_base, 180)
    image_paths['up_right_water'] = pygame.transform.rotate(down_right_water_base, ANTI_CLOCKWISE)
    image_paths['up_right'] = pygame.transform.rotate(down_right_base, ANTI_CLOCKWISE)

    #set T shape images
    image_paths['up_down_left_water'] = pygame.transform.rotate(up_down_right_water_base, 180)
    image_paths['up_down_left'] = pygame.transform.rotate(up_down_right_base, 180)
    image_paths['left_right_up_water'] = pygame.transform.rotate(up_down_right_water_base, ANTI_CLOCKWISE)
    image_paths['left_right_up'] = pygame.transform.rotate(up_down_right_base, ANTI_CLOCKWISE)
    image_paths['left_right_down_water'] = pygame.transform.rotate(up_down_right_water_base, CLOCKWISE)
    image_paths['left_right_down'] = pygame.transform.rotate(up_down_right_base, CLOCKWISE)

    return image_paths


def update_grid(grid, image_dict, all_tiles):
    for tile in all_tiles:
        x_grid = tile.x
        y_grid = tile.y
        img = None

        if len(tile.directions) == 1:
            if RIGHT in tile.directions and tile.is_water:
                img = image_dict['right_water']           
            elif RIGHT in tile.directions and not tile.is_water:
                img = image_dict['right']

            elif LEFT in tile.directions and tile.is_water:
                img = image_dict['left_water']            
            elif LEFT in tile.directions and not tile.is_water:
                img = image_dict['left']

            elif DOWN in tile.directions and tile.is_water:
                img = image_dict['down_water']
            elif DOWN in tile.directions and not tile.is_water:
                img = image_dict['down']
            
            elif UP in tile.directions and tile.is_water:
                img = image_dict['up_water']
            elif UP in tile.directions and not tile.is_water:
                img = image_dict['up']


        elif len(tile.directions) == 2 and (list(tile.directions.keys())[0] + 2) % 4 in tile.directions:
            if LEFT in tile.directions and tile.is_water:
                img = image_dict['left_right_water']
            elif LEFT in tile.directions and not tile.is_water:
                img = image_dict['left_right']
            
            elif UP in tile.directions and tile.is_water:
                img = image_dict['up_down_water']
            elif UP in tile.directions and not tile.is_water:
                img = image_dict['up_down']


        elif len(tile.directions) == 2:
            if UP in tile.directions and RIGHT in tile.directions and tile.is_water:
                img = image_dict['up_right_water']
            elif UP in tile.directions and RIGHT in tile.directions and not tile.is_water:
                img = image_dict['up_right']
            
            elif RIGHT in tile.directions and DOWN in tile.directions and tile.is_water:
                img = image_dict['down_right_water']
            elif RIGHT in tile.directions and DOWN in tile.directions and not tile.is_water:
                img = image_dict['down_right']
            
            elif DOWN in tile.directions and LEFT in tile.directions and tile.is_water:
                img = image_dict['down_left_water']
            elif DOWN in tile.directions and LEFT in tile.directions and not tile.is_water:
                img = image_dict['down_left']

            elif LEFT in tile.directions and UP in tile.directions and tile.is_water:
                img = image_dict['up_left_water']
            elif LEFT in tile.directions and UP in tile.directions and not tile.is_water:
                img = image_dict['up_left']
            
        else:
            if UP in tile.directions and DOWN in tile.directions and RIGHT in tile.directions and tile.is_water:
                img = image_dict['up_down_right_water']
            elif UP in tile.directions and DOWN in tile.directions and RIGHT in tile.directions and not tile.is_water:
                img = image_dict['up_down_right']

            elif UP in tile.directions and DOWN in tile.directions and LEFT in tile.directions and tile.is_water:
                img = image_dict['up_down_left_water']
            elif UP in tile.directions and DOWN in tile.directions and LEFT in tile.directions and not tile.is_water:
                img = image_dict['up_down_left']

            elif LEFT in tile.directions and RIGHT in tile.directions and UP in tile.directions and tile.is_water:
                img = image_dict['left_right_up_water']
            elif LEFT in tile.directions and RIGHT in tile.directions and UP in tile.directions and not tile.is_water:
                img = image_dict['left_right_up']

            elif LEFT in tile.directions and RIGHT in tile.directions and DOWN in tile.directions and tile.is_water:
                img = image_dict['left_right_down_water']
            elif LEFT in tile.directions and RIGHT in tile.directions and DOWN in tile.directions and not tile.is_water:
                img = image_dict['left_right_down']

        grid[x_grid][y_grid] = img

    return grid, all_tiles