import os
from typing import List, Tuple

# Function to read a file and return its contents as a list of strings
def read_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Function to read the grid from a file
def get_grid(file_name: str) -> List[str]:
    return read_file(os.path.join(os.path.dirname(__file__), file_name))

# Function to check if the diagonals of a 3x3 section match "MAS" or "SAM"
def diagonals_match(grid: List[str], x: int, y: int, valid_sequences: List[str]) -> bool:
    diagonal1 = [grid[x-1][y-1], grid[x][y], grid[x+1][y+1]]  # Top-left to bottom-right
    diagonal2 = [grid[x-1][y+1], grid[x][y], grid[x+1][y-1]]  # Top-right to bottom-left
    return "".join(diagonal1) in valid_sequences and "".join(diagonal2) in valid_sequences

# Function to search for all matching patterns in the grid
def find_matching_patterns(grid: List[str], valid_sequences: List[str]) -> List[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    filled_pattern_positions = []
    for x in range(1, rows - 1):  # Avoid edges, as the center needs neighbors
        for y in range(1, cols - 1):
            if diagonals_match(grid, x, y, valid_sequences):
                filled_pattern_positions.append((x, y))  # Record the center of the matching 3x3 section
    return filled_pattern_positions

# Function to visualize the matching sections
def display_matches(grid: List[str], matches: List[Tuple[int, int]]) -> None:
    visual_grid = [list(row) for row in grid]  # Convert grid to a mutable 2D list
    for x, y in matches:
        visual_grid[x][y] = '*'  # Mark the center of each matching 3x3 section with '*'
    print("\nGrid with Matches Marked:")
    for row in visual_grid:
        print("".join(row))

def main():
    grid = get_grid("day4_full_1.txt")
    valid_sequences = ["MAS", "SAM"]
    matches = find_matching_patterns(grid, valid_sequences)
    
    print("Matching 3x3 Sections Found:")
    for pos in matches:
        print(f"Center of 3x3 Section: {pos} (Row: {pos[0]}, Column: {pos[1]})")
    
    display_matches(grid, matches)
    print(f"Found {len(matches)} matches")

if __name__ == "__main__":
    main()
