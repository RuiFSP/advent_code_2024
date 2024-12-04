import os
from typing import List, Tuple

def read_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().splitlines()

def get_grid(file_name: str) -> List[str]:
    return read_file(os.path.join(os.path.dirname(__file__), file_name))

def check_word(grid: List[str], word: str, x: int, y: int, direction: Tuple[int, int]) -> bool:
    rows, cols = len(grid), len(grid[0])
    dx, dy = direction
    for i in range(len(word)):
        nx, ny = x + i * dx, y + i * dy
        if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] != word[i]:
            return False
    return True

def find_word_positions(grid: List[str], word: str, directions: List[Tuple[int, int]]) -> List[Tuple[int, int, Tuple[int, int]]]:
    rows, cols = len(grid), len(grid[0])
    found_positions = []
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == word[0]:  # Start with the first letter
                for direction in directions:
                    if check_word(grid, word, x, y, direction):
                        found_positions.append((x, y, direction))
    return found_positions



def main():
    grid = get_grid("day4_full_1.txt")
    word = "XMAS"
    directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (1, 1),  # Diagonal Down-Right
        (1, -1), # Diagonal Down-Left
        (0, -1), # Left
        (-1, 0), # Up
        (-1, -1),# Diagonal Up-Left
        (-1, 1)  # Diagonal Up-Right
    ]
    found_positions = find_word_positions(grid, word, directions)
    print(len(found_positions))

if __name__ == "__main__":
    main()
