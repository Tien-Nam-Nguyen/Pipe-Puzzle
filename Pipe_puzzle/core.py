import random
import time

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
        self.watered_from = None
        
        self.directions = {}
        self.x = x
        self.y = y



    def set_gate(self, direction):
        if self.gate <= 4 and self.gate > 1 and direction not in self.directions:

            self.directions[direction] = False
            
            self.gate -= 1

        return self
    

    def rotate_right(self, src=None, all_tiles=None):
        new_directions = {}

        for ele in self.directions:
            new_directions[(ele + 1) % 4] = False
        
        self.directions = new_directions

        if src and all_tiles:
            return flow(src, all_tiles)
    
    
    def rotate_left(self, src=None, all_tiles=None):
        new_directions = {}

        for ele in self.directions:
            new_directions[(ele + 3) % 4] = False
        
        self.directions = new_directions

        if src and all_tiles:
            return flow(src, all_tiles)




def flow(start, all_tiles):
    num_head = 0
    num_wall = 0
    num_non_leak = 0
    num_water = 0
    num_invalid_deadend = 0
    num_loop = 0

    # Reset board state
    for tile in all_tiles:
        tile.is_water = False
        for key in tile.directions:
            tile.directions[key] = False    
            tile.watered_from = None
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
            num_invalid_deadend += 1
        
        
        # Compute number of closed head
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
                all_tiles[idx].watered_from = (tile.x, tile.y)
                queue.append(all_tiles[idx])
            
            if idx != -1 and (direction + 2) % 4 in all_tiles[idx].directions and all_tiles[idx] in visited and \
                (all_tiles[idx].x != tile.watered_from[0] or all_tiles[idx].y != tile.watered_from[1]):
                num_loop += 1

        num_water += 1


    all_tiles[0].is_water = True
    return num_head - num_non_leak, GRID_SIZE**2 - num_water, num_wall, num_invalid_deadend, num_loop



def generate_game_state(x_source, y_source, starts, mode='a_star'):   # [(x, y, direction)]

    src = Tile(x_source, y_source, is_source=True)
    for way in starts:
        src.set_gate(way)

    stack = [src]
    all_tiles = [src]
    all_possible_directions = [UP, DOWN, RIGHT, LEFT]
    src_opened_gate = [way for way in src.directions]

    while len(stack) != 0:
        if len(src_opened_gate) > 0:
            tile = src
        else:
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
    num_leak, num_no_water, num_wall, num_invalid_deadend, num_loop = 0, 0, 0, 0, 0

    for i, tile in enumerate(all_tiles):
        if tile.is_source:
            continue

        rotate_time = random.randrange(4)
        if i < len(all_tiles) - 5 and mode == 'dfs':
            rotate_time = 0
        
        if mode == 'dfs' and i >= len(all_tiles) - 5:
            rotate_time = random.randrange(4)

        for i in range(rotate_time):
            num_leak, num_no_water, num_wall, num_invalid_deadend, num_loop = tile.rotate_right(src, all_tiles) 


    print(f'-------------------{num_leak}--------------{num_no_water}---------------{num_wall}---------{num_invalid_deadend}----------')
    for ele in all_tiles:
        print(f'ele: {ele.x} {ele.y} {ele.directions} {ele.is_water} {ele.is_source}') 

    
    return num_leak, num_no_water, num_wall, num_invalid_deadend, num_loop, all_tiles
        
    


def algo(all_tiles, num_opened_head_, num_no_water_, num_wall_, num_invalid_deadend_, num_loop_):
    # 
    checking_states = []        # [(state, hn, instructions, gn)]
    hn = num_opened_head_ / 2 + num_no_water_ + num_wall_ * 5 + num_invalid_deadend_ * 5 + num_loop_ * 3
    chosen_state = (all_tiles, hn, [], 0)
    visited = [chosen_state]

    while not reach_goal(chosen_state):
        

        # Loop through all possible right states
        for i, _ in enumerate(chosen_state[0]):
            
            right_lst = list_copy(chosen_state[0])
            src = right_lst[0]
            # Rotate right state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = right_lst[i].rotate_right(src, right_lst)
            hn = num_opened_head / 2 + num_no_water  + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            gn = chosen_state[3] + 1            # chosen_state[3]: previous gn
            instructions = chosen_state[2].copy()
            instructions.append((right_lst[i].x, right_lst[i].y, 'right'))

            if not is_visited((right_lst, hn, instructions, gn), visited):
                checking_states.append((right_lst, hn, instructions, gn))


        
            left_lst = list_copy(chosen_state[0])
            src = left_lst[0]
            # Rotate left state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = left_lst[i].rotate_left(src, left_lst)
            hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            gn = chosen_state[3] + 1
            instructions = chosen_state[2].copy()
            instructions.append((left_lst[i].x, left_lst[i].y, 'left'))

            
            if not is_visited((left_lst, hn, instructions, gn), visited):
                checking_states.append((left_lst, hn, instructions, gn))

            
            double_lst = list_copy(chosen_state[0])
            src = double_lst[0]
            # Rotate left state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_left(src, double_lst)
            src = double_lst[0]
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_left(src, double_lst)
            hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            gn = chosen_state[3] + 1
            instructions = chosen_state[2].copy()
            instructions.append((double_lst[i].x, double_lst[i].y, 'left left'))

    
            if not is_visited((double_lst, hn, instructions, gn), visited):
                checking_states.append((double_lst, hn, instructions, gn))
    
    
        curr_min = 1_000_000
        # print(f'Check: {chosen_state[1]} {len(checking_states)}')

        for state in checking_states:
            fn = state[1] + state[3]
            if fn <= curr_min:
                curr_min = fn
                chosen_state = state
        
        if len(checking_states) != 0:
            checking_states.remove(chosen_state)
            
        visited.append(chosen_state)
        
        if len(checking_states) == 0:
            break
        

    return chosen_state[2], len(checking_states) + len(visited)            # return a list of instructions to get to the goal state
        


def blind_search(all_tiles):
    checking_states = []        # [(state, hn, instructions, gn)]
    chosen_state = (all_tiles, -1, [], 0)
    visited = [chosen_state]


    while not reach_goal(chosen_state): 
        print(f'H(n): {chosen_state[1]}; Number of states: {len(checking_states) + len(visited)}') 
        for i, _ in enumerate(chosen_state[0]):
            right_lst = list_copy(chosen_state[0])
            src = right_lst[0]
            # Rotate right state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = right_lst[i].rotate_right(src, right_lst)
            hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            instructions = chosen_state[2].copy()
            instructions.append((right_lst[i].x, right_lst[i].y, 'right'))

            if not is_visited((right_lst, hn, instructions, 0), visited):
                checking_states.append((right_lst, hn, instructions, 0))


        
            left_lst = list_copy(chosen_state[0])
            src = left_lst[0]
            # Rotate left state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = left_lst[i].rotate_left(src, left_lst)
            hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            instructions = chosen_state[2].copy()
            instructions.append((left_lst[i].x, left_lst[i].y, 'left'))

            
            if not is_visited((left_lst, hn, instructions, 0), visited):
                checking_states.append((left_lst, hn, instructions, 0))

            
            double_lst = list_copy(chosen_state[0])
            src = double_lst[0]
            # Rotate left state
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_left(src, double_lst)
            src = double_lst[0]
            num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_left(src, double_lst)
            hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
            instructions = chosen_state[2].copy()
            instructions.append((double_lst[i].x, double_lst[i].y, 'left left'))

    
            if not is_visited((double_lst, hn, instructions, 0), visited):
                checking_states.append((double_lst, hn, instructions, 0))


        chosen_state = checking_states.pop()
        visited.append(chosen_state)
        if len(checking_states) == 0:
            break

    return chosen_state[2], len(checking_states) + len(visited)


def list_copy(lst):
    ls = []
    for ele in lst:
        ls.append(create_tile_copy(ele))

    return ls


def create_tile_copy(tile):
    tile_copy = Tile(tile.x, tile.y, tile.is_source, tile.is_water)
    tile_copy.gate = tile.gate
    tile_copy.directions = dict(tile.directions)
    return tile_copy


def is_visited(state, visited):
    # state = (tiles, hn, instruction, gn)
    # visited = [(tiles, hn, instruction, gn)]
    
    for visited_tiles, _, _, _ in visited:
        count = 0
        for visited_tile, tile in zip(visited_tiles, state[0]):
            if is_equal_tiles(visited_tile, tile):
                count += 1

        if count == len(state[0]):
            return True
            
    return False
    

def is_equal_tiles(tile1, tile2):
    if tile1.x == tile2.x and tile1.y == tile2.y and len(tile1.directions) == len(tile2.directions) and tile1.is_water == tile2.is_water:
        for key, val in tile1.directions.items():
            if key not in tile2.directions or tile2.directions[key] != val:
                return False
    else:
        return False
        
    return True


def reach_goal(chosen_state):
    if chosen_state[1] == 0:
        return True
    
    return False



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




def init_and_get_solution(grid_size, mode='a_star'):
    global GRID_SIZE
    GRID_SIZE = grid_size
    num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop, all_tiles = 1, None, None, None, None, None

    while num_opened_head % 2 == 1 or mode != 'a_star':
        print('try')
        x = random.randrange(1, GRID_SIZE - 1)
        y = random.randrange(1, GRID_SIZE - 1)
        head = random.randrange(2, 4)
        if mode == 'dfs':
            head = 3
        directions = []
        direction_choices = [UP, DOWN, LEFT, RIGHT]

        for _ in range(head):
            direction = random.choice(direction_choices)
            directions.append(direction)
            direction_choices.remove(direction)

        num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop, all_tiles = generate_game_state(x, y, directions, mode=mode)
        if num_no_water <= 5:
            mode = 'a_star'

    
    start_time = time.time()
    instructions, num_state = algo(all_tiles=all_tiles, num_opened_head_=num_opened_head, num_no_water_=num_no_water, num_wall_=num_wall, num_invalid_deadend_=num_invalid_deadend, num_loop_=num_loop)
    total_time = time.time() - start_time
    print(f"A* Success !! Algorith run in {total_time} seconds with {num_state} states")
    for instruction in instructions:
        print(f'do {instruction[0]}  {instruction[1]}  {instruction[2]}')
    
    return all_tiles, instructions, num_state, total_time
    



# if __name__ == '__main__':
#     start_time = time.time()
#     all_tiles, instructions, num_state, total_time = init_and_get_solution(3, mode='dfs')
#     instructions, num_state = blind_search(all_tiles=all_tiles)
#     print(f"DFS Success !! Algorith run in {time.time() - start_time} seconds with {num_state} states")
#     for instruction in instructions:
#         print(f'do {instruction[0]}  {instruction[1]}  {instruction[2]}')

