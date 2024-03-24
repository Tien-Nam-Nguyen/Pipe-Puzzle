import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

GRID_SIZE = 4

class Tile:

    def __init__(self, x, y, is_source=False, is_water=False):
        self.is_water = is_water
        self.is_source = is_source
        self.gate = 4
        
        self.directions = {}
        self.x = x
        self.y = y



    def set_gate(self, direction):
        if self.gate <= 4 and self.gate > 1 and direction not in self.directions:

            self.directions[direction] = False
            
            self.gate -= 1

        return self
    

    def rotate(self, src=None, all_tiles=None):
        new_directions = {}

        for ele in self.directions:
            new_directions[(ele + 1) % 4] = False
        
        self.directions = new_directions

        if src and all_tiles:
            return flow(src, all_tiles)




def exist(x_target, y_target, stack):
    if x_target < 0 or y_target < 0 or x_target >= GRID_SIZE or y_target >= GRID_SIZE:
        return True
    
    for tile in stack:
        if tile.x == x_target and tile.y == y_target:
            return True

    return False


def get_tile_index(x, y, stack):
    for i, ele in enumerate(stack):
        if ele.x == x and ele.y == y:
            return i

    return -1


def flow(start, all_tiles):
    num_head = 0
    num_wall = 0
    num_non_leak = 0
    num_water = 0

    # Reset board state
    for tile in all_tiles:
        tile.is_water = False
        for key in tile.directions:
            tile.directions[key] = False    
            num_head += 1
        
        if UP in tile.directions and tile.x == 0: 
            num_wall += 1
        
        if DOWN in tile.directions and tile.x == GRID_SIZE - 1:
            num_wall += 1

        if RIGHT in tile.directions and tile.y == GRID_SIZE - 1:
            num_wall += 1

        if LEFT in tile.directions and tile.y == 0:
            num_wall += 1

        
        side_idxs = []
        if UP in tile.directions:
            side_idxs.append((UP, get_tile_index(tile.x - 1, tile.y, all_tiles)))

        if DOWN in tile.directions:
            side_idxs.append((DOWN, get_tile_index(tile.x + 1, tile.y, all_tiles)))

        if LEFT in tile.directions:
            side_idxs.append((LEFT, get_tile_index(tile.x, tile.y - 1, all_tiles)))
            
        if RIGHT in tile.directions:
            side_idxs.append((RIGHT, get_tile_index(tile.x, tile.y + 1, all_tiles)))

            
        if len(tile.directions) == 1 and side_idxs[0][1] != -1 and len(all_tiles[side_idxs[0][1]].directions) == 1:
            num_wall += 1
        
        for way, index in side_idxs:
            if index != -1 and (way + 2) % 4 in all_tiles[index].directions:
                tile.directions[way] = True
                num_non_leak += 1

        
        

    queue = [start]
    visited = []
    while len(queue) != 0:
        tile = queue.pop(0)
        visited.append(tile)
        for direction in tile.directions:
            idx = -1
            if direction == UP:
                idx = get_tile_index(tile.x - 1, tile.y, all_tiles)
            
            elif direction == DOWN:
                idx = get_tile_index(tile.x + 1, tile.y, all_tiles)

            elif direction == LEFT:
                idx = get_tile_index(tile.x, tile.y - 1, all_tiles)

            else:
                idx = get_tile_index(tile.x, tile.y + 1, all_tiles)

            if idx != -1 and (direction + 2) % 4 in all_tiles[idx].directions and all_tiles[idx] not in visited:
                all_tiles[idx].is_water = True
                queue.append(all_tiles[idx])
            

        num_water += 1


    all_tiles[0].is_water = True
    return num_head - num_non_leak, GRID_SIZE**2 - num_water, num_wall



def generate_game_state(x_source, y_source, starts):   # [(x, y, direction)]

    src = Tile(x_source, y_source, is_source=True)
    for way in starts:
        src.set_gate(way)

    stack = [src]
    all_tiles = [src]
    all_possible_directions = [UP, DOWN, RIGHT, LEFT]
    src_opened_gate = [way for way in src.directions]

    while len(stack) != 0:
        tile = random.choice(stack)

        opened_gates = []
    
        for direction in all_possible_directions:
        
            if direction not in tile.directions:
                opened_gates.append(direction)

        if tile.is_source:
            opened_gates = src_opened_gate
    

        invalid_directions = []
        for direction in opened_gates:
            if (direction == LEFT and exist(tile.x, tile.y - 1, all_tiles)) or (direction == RIGHT and exist(tile.x, tile.y + 1, all_tiles)) \
                    or (direction == UP and exist(tile.x - 1, tile.y, all_tiles)) or (direction == DOWN and exist(tile.x + 1, tile.y, all_tiles)):
    
                invalid_directions.append(direction)


        if len(invalid_directions) == len(opened_gates) or (tile.gate == 1 and not tile.is_source) or (tile.is_source and len(src_opened_gate) == 0):
            stack.remove(tile)
            continue
    

        for direction in invalid_directions:
            opened_gates.remove(direction)


        chosen_direction = random.choice(opened_gates)
        if not tile.is_source:
            tile.set_gate(chosen_direction)
        else:
            src_opened_gate.remove(chosen_direction)


        newTile = None
        if chosen_direction == UP:
            newTile = Tile(tile.x - 1, tile.y).set_gate(DOWN)
    
        elif chosen_direction == DOWN:
            newTile = Tile(tile.x + 1, tile.y).set_gate(UP)

        elif chosen_direction == RIGHT:
            newTile = Tile(tile.x, tile.y + 1).set_gate(LEFT)

        else:
            newTile = Tile(tile.x, tile.y - 1).set_gate(RIGHT)

        stack.append(newTile)
        all_tiles.append(newTile)


    for ele in all_tiles:
        print(f'ele: {ele.x} {ele.y} {ele.directions}') 
    

    # Random rotate and fill water
    num_leak, num_no_water, num_wall = 0, 0, 0

    for tile in all_tiles:
        if tile.is_source:
            continue

        rotate_time = random.randrange(4)

        for i in range(rotate_time):
            num_leak, num_no_water, num_wall = tile.rotate(src, all_tiles) 


    print(f'-------------------{num_leak}--------------{num_no_water}---------------{num_wall}--------------')
    for ele in all_tiles:
        print(f'ele: {ele.x} {ele.y} {ele.directions} {ele.is_water}') 
        
    


def algo(num_opened_head, num_no_water, num_wall_and_deadend):
    fn = num_opened_head / 2 + num_no_water + num_wall_and_deadend
    while True:
        pass


def main():
    generate_game_state(1, 1, [UP, DOWN, RIGHT])


if __name__ == '__main__':
    main()

