import os

def read_input(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def move(position, direction):
    moves = {'^': (0,-1), '>': (1,0), 'v': (0,1), '<': (-1,0)}
    return (position[0] + moves[direction][0], position[1] + moves[direction][1])

def initial_position_guard(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                return (x,y)
    return None

def update_grid(grid, position, new_position, direction):
    x_old, y_old = position
    x_new, y_new = new_position
    grid[y_old][x_old] = '.'
    grid[y_new][x_new] = direction
    return grid

def change_direction(direction):
    directions = '^>v<'
    return directions[(directions.index(direction) + 1) % 4]


def print_grid(grid, position, direction):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) == position:
                print(direction, end='')
            else:
                print(cell, end='')
        print()


def grid_game_status(grid, position):
    direction = '^'
    visited = set()
    steps = 0
    max_steps = 10000  # Arbitrary large number to detect infinite loops

    while steps < max_steps:
        visited.add(position)
        next_position = move(position, direction)
        x, y = next_position

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            break

        if grid[y][x] == '.':
            grid = update_grid(grid, position, next_position, direction)
            position = next_position
        else:
            direction = change_direction(direction)
            next_position = move(position, direction)
            grid = update_grid(grid, position, next_position, direction)
            position = next_position
        
        steps += 1
    
    if steps >= max_steps:
        return list(visited), True  # Return True if stuck
    else:
        #print_grid(grid, position, direction)
        return list(visited), False  # Return False if not stuck

def initial_obstacles(grid):
    return [(x,y) for y,row in enumerate(grid) for x,cell in enumerate(row) if cell == '#']


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'day6_full_1.txt')
    initial_grid = read_input(file_path)
    
    # Position of the guard
    guard_init_position = initial_position_guard(initial_grid)

    visited_positions_coords, _ = grid_game_status(initial_grid, guard_init_position)
    print(f"The guard visited {len(visited_positions_coords)} locations")
    #print("Visited positions:", visited_positions_coords)

    obstacles = initial_obstacles(initial_grid)
    #print("Initial obstacles:", obstacles)
    
    counter = 1
    stuck_counter = 0
    
    for (x, y) in visited_positions_coords:
        if (x, y) == guard_init_position:
            continue  # Skip if the new obstacle is at the guard's initial position
        
        new_obstacle = (x, y)
        
        # Read the input file again
        initial_grid = read_input(file_path)
        
        #print(f"\nAdding new obstacle at {new_obstacle}\n")
        
        # Adding the new obstacle
        initial_grid[y][x] = '#'
        
        # Position of the guard
        guard_init_position = initial_position_guard(initial_grid)
        
        # Test the new grid
        visited_positions_coords, is_stuck = grid_game_status(initial_grid, guard_init_position)
        
        if is_stuck:
            stuck_counter += 1
            #print(f"The guard got stuck with the obstacle at {new_obstacle}")
        
        counter += 1
        
    print(f"I've printed all grids for all the obstacles {counter} times")
    print(f"The guard got stuck {stuck_counter} times")










