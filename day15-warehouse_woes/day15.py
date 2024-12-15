from collections import deque
import os
from typing import List, Tuple

DIRECTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}

WALL = "#"
EMPTY = "."
TRAIN_HEAD = "@"
TRAIN_PART1 = "O"
TRAIN_PART2_LEFT = "["
TRAIN_PART2_RIGHT = "]"

def read_input(file_name: str) -> str:
    """
    Reads the input file and returns its content as a string.
    """
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        return file.read().strip()

def initialize_grid(warehouse_map: str, part2: bool = False) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Initializes the grid based on the warehouse map and part2 flag.
    
    Args:
        warehouse_map (str): The warehouse map as a string.
        part2 (bool): Flag indicating whether to use part2 logic.
    
    Returns:
        tuple: The initialized grid and the position of the train head.
    """
    grid = []
    train_head_pos = None
    for r, line in enumerate(warehouse_map.split("\n")):
        row = []
        for c, char in enumerate(line):
            if part2:
                if char == WALL:
                    row.extend([WALL, WALL])
                elif char == TRAIN_PART1:
                    row.extend([TRAIN_PART2_LEFT, TRAIN_PART2_RIGHT])
                elif char == EMPTY:
                    row.extend([EMPTY, EMPTY])
                elif char == TRAIN_HEAD:
                    row.extend([TRAIN_HEAD, EMPTY])
                    train_head_pos = (r, c * 2)
            else:
                row.append(char)
                if char == TRAIN_HEAD:
                    train_head_pos = (r, c)
        grid.append(row)
    return grid, train_head_pos

def move_train(grid: List[List[str]], moves: List[str], train_head_pos: Tuple[int, int], part2: bool = False) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Moves the train on the grid based on the moves and part2 flag.
    
    Args:
        grid (list): The grid representing the warehouse.
        moves (list): List of moves to be made.
        train_head_pos (tuple): The position of the train head.
        part2 (bool): Flag indicating whether to use part2 logic.
    
    Returns:
        tuple: The updated grid and the new position of the train head.
    """
    for move in moves:
        dr, dc = DIRECTIONS[move]
        valid_move, train_positions = get_train_positions(grid, move, train_head_pos, part2)
        if not valid_move:
            continue
        for pr, pc in train_positions[::-1]:
            if grid[pr][pc] == TRAIN_HEAD:
                train_head_pos = (train_head_pos[0] + dr, train_head_pos[1] + dc)
            grid[pr + dr][pc + dc] = grid[pr][pc]
            grid[pr][pc] = EMPTY
    return grid, train_head_pos

def get_train_positions(grid: List[List[str]], move: str, train_head_pos: Tuple[int, int], part2: bool) -> Tuple[bool, List[Tuple[int, int]]]:
    """
    Gets the positions of the train based on the move and part2 flag.
    
    Args:
        grid (list): The grid representing the warehouse.
        move (str): The move to be made.
        train_head_pos (tuple): The position of the train head.
        part2 (bool): Flag indicating whether to use part2 logic.
    
    Returns:
        tuple: A boolean indicating if the move is valid and the positions of the train.
    """
    if part2:
        return get_train_positions_part2(grid, move, train_head_pos)
    else:
        return get_train_positions_part1(grid, move, train_head_pos)

def get_train_positions_part1(grid: List[List[str]], move: str, train_head_pos: Tuple[int, int]) -> Tuple[bool, List[Tuple[int, int]]]:
    """
    Gets the positions of the train for part1 logic.
    
    Args:
        grid (list): The grid representing the warehouse.
        move (str): The move to be made.
        train_head_pos (tuple): The position of the train head.
    
    Returns:
        tuple: A boolean indicating if the move is valid and the positions of the train.
    """
    train_positions = []
    dr, dc = DIRECTIONS[move]
    tr, tc = train_head_pos
    while True:
        if grid[tr][tc] in {TRAIN_HEAD, TRAIN_PART1}:
            train_positions.append((tr, tc))
        elif grid[tr][tc] == WALL:
            return False, []
        elif grid[tr][tc] == EMPTY:
            return True, train_positions
        tr += dr
        tc += dc
    return False, []

def get_train_positions_part2(grid: List[List[str]], move: str, train_head_pos: Tuple[int, int]) -> Tuple[bool, List[Tuple[int, int]]]:
    """
    Gets the positions of the train for part2 logic.
    
    Args:
        grid (list): The grid representing the warehouse.
        move (str): The move to be made.
        train_head_pos (tuple): The position of the train head.
    
    Returns:
        tuple: A boolean indicating if the move is valid and the positions of the train.
    """
    queue = deque([train_head_pos])
    seen = set()
    train_positions = []
    dr, dc = DIRECTIONS[move]
    while queue:
        r, c = queue.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))
        if grid[r][c] == EMPTY:
            continue
        elif grid[r][c] == WALL:
            return False, []
        train_positions.append((r, c))
        current_part = grid[r][c]
        assert current_part in {TRAIN_PART2_LEFT, TRAIN_PART2_RIGHT, TRAIN_HEAD}
        if current_part == TRAIN_PART2_LEFT:
            if (r, c + 1) not in seen and move != ">":
                queue.append((r, c + 1))
        elif current_part == TRAIN_PART2_RIGHT:
            if (r, c - 1) not in seen and move != "<":
                queue.append((r, c - 1))
        queue.append((r + dr, c + dc))
    return True, train_positions

def calculate_answer(grid: List[List[str]], part2: bool = False) -> int:
    """
    Calculates the answer based on the grid and part2 flag.
    
    Args:
        grid (list): The grid representing the warehouse.
        part2 (bool): Flag indicating whether to use part2 logic.
    
    Returns:
        int: The calculated answer.
    """
    answer = 0
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if part2 and char == TRAIN_PART2_LEFT:
                answer += 100 * r + c
            elif not part2 and char == TRAIN_PART1:
                answer += 100 * r + c
    return answer

def solve(file_name: str, part2: bool = False) -> None:
    """
    Solves the problem for the given input file and part2 flag.
    
    Args:
        file_name (str): The name of the input file.
        part2 (bool): Flag indicating whether to use part2 logic.
    """
    warehouse_map, move_sequence = read_input(file_name).split("\n\n")
    grid, train_head_pos = initialize_grid(warehouse_map, part2)
    moves = [m for line in move_sequence.split("\n") for m in line]
    grid, train_head_pos = move_train(grid, moves, train_head_pos, part2)
    answer = calculate_answer(grid, part2)
    print("Answer:", answer)

if __name__ == "__main__":
    file_names = ['day15_simple.txt', 'day15_full.txt']
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Solving for file {file_name}")
            solve(file_name)
            solve(file_name, part2=True)
        else:
            print(f"File {file_name} does not exist.")
