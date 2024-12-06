import os


def read_input():
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]
        

def move(position, direction):
    if direction == '^':
        return (position[0], position[1] - 1)
    elif direction == '>':
        return (position[0] + 1, position[1])
    elif direction == 'v':
        return (position[0], position[1] + 1)
    elif direction == '<':
        return (position[0] - 1, position[1])


def initial_position_guard(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                print('Initial position:', (x, y))
                return (x, y)
    return None


def print_grid(grid, position, direction):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) == position:
                print(direction, end='')
            else:
                print(cell, end='')
        print()


def update_grid(grid, position):
    x, y = position
    grid[y][x] = '.'
    return grid

def update_guard_position(grid, old_position, new_position, direction):
    x_old, y_old = old_position
    x_new, y_new = new_position
    grid[y_old][x_old] = '.'
    grid[y_new][x_new] = direction
    return grid

def change_direction(direction):
    if direction == '^':
        return '>'
    elif direction == '>':
        return 'v'
    elif direction == 'v':
        return '<'
    elif direction == '<':
        return '^'


def grid_game_status(grid):
    position = initial_position_guard(grid)
    direction = '^'
    visited = set()

    while True:
        visited.add(position)
        next_position = move(position, direction)
        
        #print('Next position:', next_position)
        
        x, y = next_position

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            break
        
        if grid[y][x] == '.':
            grid = update_grid(grid, position)
            position = next_position
            #print('New position:', position)
        else:
            #print('Current position:', position)
            grid = update_grid(grid, position)  # Update the current position to "."
            direction = change_direction(direction)
            next_position = move(position, direction)
            grid = update_guard_position(grid, position, next_position, direction)
            position = next_position
            #print('New position for guard after update:', position)   
                   
        #print_grid(grid, position, direction)
        #print()
        print(f"The guard visited", len(visited) + 1, "locations")


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'day6_full_1.txt')
    grid = read_input()
    grid_game_status(grid)
