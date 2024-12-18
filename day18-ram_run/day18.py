import os
from heapq import heappush, heappop
from typing import List, Set, Tuple

def parse_coordinates(filename: str) -> List[Tuple[int, int]]:
    """
    Reads the input file and returns a list of coordinate tuples.
    
    Args:
        filename (str): The name of the input file.
    
    Returns:
        List[Tuple[int, int]]: A list of (x, y) coordinate tuples.
    """
    with open(filename, 'r') as file:
        return [(int(x), int(y)) for x, y in [line.strip().split(',') for line in file]]

def calculate_manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calculates the Manhattan distance between two points.
    
    Args:
        x1 (int): X-coordinate of the first point.
        y1 (int): Y-coordinate of the first point.
        x2 (int): X-coordinate of the second point.
        y2 (int): Y-coordinate of the second point.
    
    Returns:
        int: The Manhattan distance between the two points.
    """
    return abs(x1 - x2) + abs(y1 - y2)

def find_valid_neighbors(x: int, y: int, blocked_coords: Set[Tuple[int, int]], max_coord: int) -> List[Tuple[int, int]]:
    """
    Gets the valid neighboring coordinates for a given point.
    
    Args:
        x (int): X-coordinate of the current point.
        y (int): Y-coordinate of the current point.
        blocked_coords (Set[Tuple[int, int]]): Set of blocked coordinates.
        max_coord (int): Maximum coordinate value.
    
    Returns:
        List[Tuple[int, int]]: A list of valid neighboring coordinates.
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x <= max_coord and 
            0 <= new_y <= max_coord and 
            (new_x, new_y) not in blocked_coords):
            neighbors.append((new_x, new_y))
    return neighbors

def find_shortest_path(blocked_coords: Set[Tuple[int, int]], max_coord: int) -> int:
    """
    Performs the A* search algorithm to find the shortest path.
    
    Args:
        blocked_coords (Set[Tuple[int, int]]): Set of blocked coordinates.
        max_coord (int): Maximum coordinate value.
    
    Returns:
        int: The length of the shortest path, or -1 if no path is found.
    """
    start = (0, 0)
    goal = (max_coord, max_coord)
    
    open_set = [(calculate_manhattan_distance(0, 0, max_coord, max_coord), start)]
    g_scores = {start: 0}
    
    while open_set:
        _, current = heappop(open_set)
        
        if current == goal:
            return g_scores[current]
            
        for neighbor in find_valid_neighbors(*current, blocked_coords, max_coord):
            tentative_g_score = g_scores[current] + 1
            
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_manhattan_distance(*neighbor, *goal)
                heappush(open_set, (f_score, neighbor))
    
    return -1

def solve_min_steps(filename: str) -> int:
    """
    Solves part 1 of the problem.
    
    Args:
        filename (str): The name of the input file.
    
    Returns:
        int: The minimum number of steps needed.
    """
    blocked_coords = set(parse_coordinates(filename)[:1024])  # Only first 1024 bytes
    return find_shortest_path(blocked_coords, 70)

def find_first_blocking_coordinate(filename: str) -> Tuple[int, int]:
    """
    Solves part 2 of the problem.
    
    Args:
        filename (str): The name of the input file.
    
    Returns:
        Tuple[int, int]: The first blocking coordinate that blocks all paths.
    """
    coordinates = parse_coordinates(filename)
    blocked_coords = set()
    
    for x, y in coordinates:
        blocked_coords.add((x, y))
        if find_shortest_path(blocked_coords, 70) == -1:
            return x, y
    
    return -1, -1

if __name__ == "__main__":
    file_names = ['day18_simple.txt', 'day18_full.txt']
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Solving for file {file_name}")
            result1 = solve_min_steps(file_name)
            print(f"Part 1: Minimum steps needed = {result1}")
            
            x, y = find_first_blocking_coordinate(file_name)
            print(f"Part 2: First blocking coordinate = {x},{y}")
            
        else:
            print(f"File {file_name} does not exist.")