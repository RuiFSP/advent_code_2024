from collections import defaultdict
from itertools import combinations
import os
from typing import Tuple, Set, Dict

def is_valid(point: Tuple[int, int], max_x: int, max_y: int) -> bool:
    """
    Check if a given point is within the bounds of a grid.

    Args:
        point (Tuple[int, int]): The point to check, represented as a tuple (x, y).
        max_x (int): The maximum x-coordinate (exclusive) of the grid.
        max_y (int): The maximum y-coordinate (exclusive) of the grid.

    Returns:
        bool: True if the point is within the bounds of the grid, False otherwise.
    """
    return 0 <= point[0] < max_x and 0 <= point[1] < max_y

def generate_antinodes(point1: Tuple[int, int], point2: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate antinodes for two given points.

    This function calculates two new points (antinodes) based on the input points.
    The new points are reflections of the input points across the midpoint of the line segment connecting them.

    Args:
        point1 (Tuple[int, int]): The first point as a tuple of (x, y) coordinates.
        point2 (Tuple[int, int]): The second point as a tuple of (x, y) coordinates.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing two new points (antinodes) as tuples of (x, y) coordinates.
    """
    new_point1 = point1[0] - (point2[0] - point1[0]), point1[1] - (point2[1] - point1[1])
    new_point2 = point2[0] - (point1[0] - point2[0]), point2[1] - (point1[1] - point2[1])
    return new_point1, new_point2

def read_antennas(file_path: str) -> Tuple[Dict[str, Set[Tuple[int, int]]], int, int]:
    """
    Reads antenna positions from a file and returns a dictionary of antenna types with their coordinates,
    along with the maximum x and y dimensions of the grid.

    Args:
        file_path (str): The path to the file containing the antenna data.

    Returns:
        Tuple[Dict[str, Set[Tuple[int, int]]], int, int]:
            - A dictionary where keys are antenna types (characters) and values are sets of (x, y) coordinates.
            - The maximum x dimension of the grid.
            - The maximum y dimension of the grid.
    """
    antennas = defaultdict(set)
    with open(file_path) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char != ".":
                    antennas[char].add((x, y))
        max_y = y + 1
        max_x = len(line.strip())
    return antennas, max_x, max_y

def part1(file_path: str) -> None:
    """
    Processes the input file to determine the number of unique antinodes generated by antenna pairs.

    Args:
        file_path (str): The path to the input file containing antenna data.

    Returns:
        int: The total number of unique antinodes generated by pairs of points from the input antennas.

    The function performs the following steps:
    1. Reads antenna data from the input file.
    2. Iterates over each antenna and generates antinodes from pairs of points.
    3. Checks if the generated antinodes are valid within the given boundaries.
    4. Adds valid antinodes to a set to ensure uniqueness.
    5. Returns the total number of unique antinodes.
    """
    antennas, max_x, max_y = read_antennas(file_path)
    antinodes = set()

    for antenna in antennas:
        for point1, point2 in combinations(antennas[antenna], 2):
            new_point1, new_point2 = generate_antinodes(point1, point2)
            if is_valid(new_point1, max_x, max_y):
                antinodes.add(new_point1)
            if is_valid(new_point2, max_x, max_y):
                antinodes.add(new_point2)

    return len(antinodes)

def generate_all_antinodes(point1: Tuple[int, int], point2: Tuple[int, int], max_x: int, max_y: int) -> Set[Tuple[int, int]]:
    """
    Generate all antinodes (points) that are collinear with two given points within a specified grid.

    An antinode is a point (x3, y3) that lies on the line defined by the points (x1, y1) and (x2, y2).
    This function finds all such points within the bounds of a grid defined by max_x and max_y.

    Args:
        point1 (Tuple[int, int]): The first point (x1, y1).
        point2 (Tuple[int, int]): The second point (x2, y2).
        max_x (int): The maximum x-coordinate value for the grid.
        max_y (int): The maximum y-coordinate value for the grid.

    Returns:
        Set[Tuple[int, int]]: A set of tuples representing the coordinates of all antinodes within the grid.
    """
    antinodes = set()
    x1, y1 = point1
    x2, y2 = point2

    for y3 in range(max_y):
        for x3 in range(max_x):
            if (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) == 0:
                antinodes.add((x3, y3))

    return antinodes

def part2(file_path: str) -> None:
    """
    Processes the input file to determine the number of unique antinodes generated by antenna pairs.

    Args:
        file_path (str): The path to the input file containing antenna data.
    Returns:
        int: The total number of unique antinodes generated by pairs of points from the input antennas.

    The function reads antenna data from the specified file, calculates all possible antinodes
    generated by pairs of points from each antenna, and prints the total number of unique antinodes.

    The input file is expected to contain antenna data in a format that can be parsed by the
    `read_antennas` function. The `generate_all_antinodes` function is used to generate antinodes
    for each pair of points.

    """
    antennas, max_x, max_y = read_antennas(file_path)
    antinodes = set()

    for antenna in antennas:
        for point1, point2 in combinations(antennas[antenna], 2):
            antinodes |= generate_all_antinodes(point1, point2, max_x, max_y)

    return len(antinodes)

if __name__ == "__main__":
    file_path_1 = os.path.join(os.path.dirname(__file__), 'day8_simple.txt')
    print("Simple Part 1:" , part1(file_path_1))
    
    file_path_2 = os.path.join(os.path.dirname(__file__), 'day8_simple.txt')
    print("Simple Part 2:" , part2(file_path_2))
    
    
    file_path = os.path.join(os.path.dirname(__file__), 'day8_full.txt')
    
    print("Part 1:" , part1(file_path))
    print("Part 2:" , part2(file_path)) 
