import os
from collections.abc import Iterator
from pathlib import Path

def read_input(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a stripped string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file with leading and trailing whitespace removed.
    """
    with open(file_path) as file:
        return file.read().strip()

def parse_grid(file_path: str) -> dict[complex, int]:
    """
    Parses the grid from the file and returns a dictionary with complex coordinates as keys and grid values as values.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        dict[complex, int]: The parsed grid.
    """
    lines = Path(file_path).read_text().splitlines()
    return {complex(row, col): int(value) for row, line in enumerate(lines) for col, value in enumerate(line)}

def find_starts(grid: dict[complex, int]) -> list[complex]:
    """
    Finds all starting points in the grid where the value is 0.

    Args:
        grid (dict[complex, int]): The grid.

    Returns:
        list[complex]: The list of starting points.
    """
    return [position for position, value in grid.items() if value == 0]

def next_valid_steps(grid: dict[complex, int], position: complex, slope: int) -> Iterator[complex]:
    """
    Generates the next valid steps from the current position.

    Args:
        grid (dict[complex, int]): The grid.
        position (complex): The current position.
        slope (int): The current slope.

    Yields:
        Iterator[complex]: The next valid steps.
    """
    directions = (1, 1j, -1, -1j)
    for step in directions:
        next_position = position + step
        if next_position in grid and grid[next_position] - slope == 1:
            yield next_position

def find_peaks(grid: dict[complex, int], position: complex, slope: int) -> set[complex]:
    """
    Recursively finds all peaks starting from the given position.

    Args:
        grid (dict[complex, int]): The grid.
        position (complex): The starting position.
        slope (int): The current slope.

    Returns:
        set[complex]: The set of peak positions.
    """
    if grid[position] == 9:
        return {position}
    return set().union(*(find_peaks(grid, next_position, slope + 1) for next_position in next_valid_steps(grid, position, slope)))

def count_routes(grid: dict[complex, int], position: complex, slope: int) -> int:
    """
    Recursively counts all routes to peaks starting from the given position.

    Args:
        grid (dict[complex, int]): The grid.
        position (complex): The starting position.
        slope (int): The current slope.

    Returns:
        int: The number of routes to peaks.
    """
    if grid[position] == 9:
        return 1
    return sum(count_routes(grid, next_position, slope + 1) for next_position in next_valid_steps(grid, position, slope))

def process_file(file_path: str) -> tuple[int, int]:
    """
    Processes the file to calculate the results for part 1 and part 2.

    Args:
        file_path (str): The path to the file to be processed.

    Returns:
        tuple[int, int]: The results for part 1 and part 2.
    """
    grid = parse_grid(file_path)
    starts = find_starts(grid)

    part1_result = sum(len(find_peaks(grid, start, slope=0)) for start in starts)
    part2_result = sum(count_routes(grid, start, slope=0) for start in starts)

    return part1_result, part2_result

if __name__ == "__main__":
    for file_name in ['day10_simple.txt', 'day10_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        part1_result, part2_result = process_file(file_path)
        
        print(f'Part 1 {file_name.split("_")[1]}: {part1_result}')
        print(f'Part 2 {file_name.split("_")[1]}: {part2_result}')