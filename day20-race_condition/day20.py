import os
from typing import Dict, List, Tuple

def read_data(file_path: str) -> List[str]:
    """
    Read and process the input data from a file.

    Args:
        file_path (str): The path to the input file.

    Returns:
        List[str]: A list of strings, each representing a line from the file.
    """
    with open(file_path) as f:
        return f.read().strip().split('\n')

def create_grid(data: List[str]) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Tuple[int, int], int]:
    """
    Create a grid from the given data and identify the start, end, and count of '.' characters.

    Args:
        data (List[str]): A list of strings representing the grid, where each string is a row.

    Returns:
        Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Tuple[int, int], int]:
            - A dictionary representing the grid with keys as (row, column) tuples and values as characters.
            - A tuple representing the coordinates of the start position 'S'.
            - A tuple representing the coordinates of the end position 'E'.
            - An integer count of the '.' characters in the grid.
    """
    grid = {}
    cnt = 2
    start = end = (0, 0)
    for r, l in enumerate(data):
        for c, v in enumerate(l):
            grid[(r, c)] = v
            if v == 'S':
                start = (r, c)
            if v == 'E':
                end = (r, c)
            if v == '.':
                cnt += 1
    return grid, start, end, cnt

def bfs(grid: Dict[Tuple[int, int], str], start: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    """
    Perform Breadth-First Search (BFS) to calculate the shortest distances from the start position
    to all other reachable positions in the grid.

    Args:
        grid (Dict[Tuple[int, int], str]): A dictionary representing the grid where keys are 
                                           coordinates (row, column) and values are characters 
                                           representing the content of the cell (e.g., '.', '#').
        start (Tuple[int, int]): The starting position in the grid as a tuple (row, column).

    Returns:
        Dict[Tuple[int, int], int]: A dictionary where keys are coordinates (row, column) and 
                                    values are the shortest distance from the start position to 
                                    that coordinate.
    """
    ds = ((1, 0), (-1, 0), (0, 1), (0, -1))
    dist_map = {start: 0}
    queue = [start]
    for r, c in queue:
        d = dist_map[(r, c)]
        for dr, dc in ds:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in dist_map and grid.get((nr, nc)) != '#':
                queue.append((nr, nc))
                dist_map[(nr, nc)] = d + 1
    return dist_map

def calculate_cheats(start_map: Dict[Tuple[int, int], int], range_limit: int) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]:
    """
    Calculate cheats based on the start map and range limit.

    Args:
        start_map (Dict[Tuple[int, int], int]): A dictionary where keys are coordinates (tuples of two integers) 
                                                and values are integers representing some value at those coordinates.
        range_limit (int): An integer representing the range limit for calculating cheats.

    Returns:
        Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]: A dictionary where keys are tuples of coordinate pairs 
                                                            and values are integers representing the calculated cheats.
    """
    ds = ((1, 0), (-1, 0), (0, 1), (0, -1))
    cheats = {}
    for r, c in start_map:
        for dr, dc in ds:
            nr, nc = r + 2 * dr, c + 2 * dc
            if (nr, nc) in start_map:
                if start_map[(r, c)] > start_map[(nr, nc)]:
                    nn = start_map[(r, c)] - start_map[(nr, nc)] - 2
                    if nn > 0:
                        cheats[((r, c), (nr, nc))] = nn
    return cheats

def calculate_cheats_extended(start_map: Dict[Tuple[int, int], int], range_limit: int) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]:
    """
    Calculate extended cheats based on the start map and range limit.

    Args:
        start_map (Dict[Tuple[int, int], int]): A dictionary where the keys are coordinates (tuples of integers) 
                                                and the values are integers representing some value at those coordinates.
        range_limit (int): The maximum range limit to consider for calculating cheats.

    Returns:
        Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]: A dictionary where the keys are tuples of coordinate pairs 
                                                            and the values are integers representing the calculated cheats.
    """
    cheats = {}
    for r, c in start_map:
        for i in range(-range_limit, range_limit + 1):
            for j in range(-range_limit, range_limit + 1):
                if abs(i) + abs(j) <= range_limit:
                    nr, nc = r + i, c + j
                    if (nr, nc) in start_map:
                        if start_map[(r, c)] > start_map[(nr, nc)]:
                            nn = start_map[(r, c)] - start_map[(nr, nc)] - abs(i) - abs(j)
                            if nn > 0:
                                cheats[((r, c), (nr, nc))] = nn
    return cheats

def count_cheats(cheats: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int], threshold: int) -> int:
    """
    Count the number of cheats that meet or exceed the threshold.

    Args:
        cheats (Dict[Tuple[Tuple[int, int], Tuple[int, int]], int]): A dictionary where the keys are tuples of tuples 
            representing coordinates, and the values are integers representing the number of cheats.
        threshold (int): The threshold number of cheats to count.

    Returns:
        int: The number of cheats that meet or exceed the threshold.
    """
    return sum(1 for n in cheats.values() if n >= threshold)


if __name__ == "__main__":
    file_names = ['day20_simple.txt','day20_full.txt']
    final_results = []
    for file_name in file_names:
        if os.path.exists(file_name):
            data = read_data(file_name)
            grid, start, end, cnt = create_grid(data)
            start_map = bfs(grid, start)

            cheats = calculate_cheats(start_map, 2)
            p1 = count_cheats(cheats, 100)

            cheats_extended = calculate_cheats_extended(start_map, 20)
            p2 = count_cheats(cheats_extended, 100)

            final_results.append((p1, p2))
        else:
            print(f"File {file_name} does not exist.")

    if final_results:
        p1, p2 = final_results[-1]
        print(f"Final Part 1 - How many cheats would save you at least 100 picoseconds?: {p1}")
        print(f"Final Part 2: - How many cheats would save you at least 100 picoseconds? {p2}")