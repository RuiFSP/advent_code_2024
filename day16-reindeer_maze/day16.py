import os
import heapq
from queue import PriorityQueue
from collections import namedtuple
from typing import List, Tuple, Generator

def parse_input(input_str: str) -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    """
    Parses the input string representing the reindeer maze and identifies the start and end positions.

    Args:
        input_str (str): A string representation of the maze where each line is a row of the maze.
                         'S' represents the start position, 'E' represents the end position, and
                         other characters represent the maze layout.

    Returns:
        tuple: A tuple containing:
            - grid (list of str): The maze grid as a list of strings.
            - start (tuple of int): The coordinates (row, column) of the start position.
            - end (tuple of int): The coordinates (row, column) of the end position.
    """
    grid = input_str.strip().split("\n")
    start = end = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
            elif cell == 'E':
                end = (r, c)
    return grid, start, end

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    Calculate the Manhattan distance between two points.

    The Manhattan distance is the sum of the absolute differences of their Cartesian coordinates.

    Parameters:
    a (tuple): The first point as a tuple of two integers (x1, y1).
    b (tuple): The second point as a tuple of two integers (x2, y2).

    Returns:
    int: The Manhattan distance between points a and b.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reindeer_maze(grid: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """
    Finds the minimum cost path in a grid from the start position to the end position,
    considering movement and rotation costs.
    Args:
        grid (list of list of str): The grid representing the maze, where '.' is a free space and '#' is an obstacle.
        start (tuple of int): The starting position in the grid as (row, col).
        end (tuple of int): The ending position in the grid as (row, col).
    Returns:
        int: The minimum cost to reach the end position from the start position. Returns -1 if no path is found.
    Raises:
        ValueError: If the start or end position is None.
    """
    if start is None or end is None:
        raise ValueError("Start or end position not found in the grid.")
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, start[0], start[1], 0))  # (cost, row, col, facing)
    
    while priority_queue:
        cost, x, y, facing = heapq.heappop(priority_queue)
        
        if (x, y) == end:
            return cost
        
        if (x, y, facing) in visited:
            continue
        visited.add((x, y, facing))
        
        # Move forward
        dx, dy = directions[facing]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != '#':
            heapq.heappush(priority_queue, (cost + 1, new_x, new_y, facing))
        
        # Rotate left and right
        for rotation in [-1, 1]:
            new_facing = (facing + rotation) % 4
            heapq.heappush(priority_queue, (cost + 1000, x, y, new_facing))
    
    return -1

def reindeer_maze_part2(grid: List[str]) -> int:
    """
    Solves the reindeer maze puzzle by finding the shortest path from the start ('S') to the end ('E').

    Args:
        grid (list of str): The maze represented as a list of strings, where each string is a row of the maze.
                            'S' represents the start position, 'E' represents the end position, and '#' represents walls.

    Returns:
        int: The number of tiles in the shortest path from 'S' to 'E'.

    Helper Functions:
        isvalid(c):
            Checks if a given complex coordinate is within the bounds of the maze.

            Args:
                c (complex): The coordinate to check.

            Returns:
                bool: True if the coordinate is within bounds, False otherwise.

        getch(c):
            Retrieves the character at a given complex coordinate in the maze.

            Args:
                c (complex): The coordinate to retrieve the character from.

            Returns:
                str: The character at the specified coordinate.

        estimate_cost(p):
            Estimates the cost to reach the end position from a given position.

            Args:
                p (complex): The current position.

            Returns:
                float: The estimated cost to reach the end position.

        make_rotations(node):
            Generates possible rotations (directions) from the current node.

            Args:
                node (Node): The current node.

            Yields:
                complex: The possible rotation directions.
    """
    board = [list(row.strip()) for row in grid]
    mx, my = len(board[0]), len(board)

    def isvalid(c: complex) -> bool:
        return 0 <= c.real < mx and 0 <= c.imag < my

    def getch(c: complex) -> str:
        return board[int(c.imag)][int(c.real)]

    start = end = None
    for y, row in enumerate(board):
        for x, ch in enumerate(row):
            if ch == "E": end = complex(x, y)
            if ch == "S": start = complex(x, y)

    def estimate_cost(p: complex) -> float:
        return 100 * (abs(p.real - end.real) + abs(p.imag - end.imag)) + 1500 * (end.imag != p.imag) + 1500 * (end.real != p.real) + abs(p.real) + abs(p - end)

    def make_rotations(node: namedtuple) -> Generator[complex, None, None]:
        if getch(node.p + node.v * 1j) != "#":
            yield 1j
        if getch(node.p + node.v * -1j) != "#":
            yield -1j

    inf = float('inf')
    strict_visited = {}
    md = inf
    best = []

    Node = namedtuple("Node", ["priority", "cost", "p", "v", "tiles"])
    Node.__lt__ = lambda self, value: self[0] < value[0]

    q = PriorityQueue()
    q.put_nowait(Node(estimate_cost(start), 0, start, 1+0j, {start}))

    while not q.empty():
        state = q.get_nowait()
        strict_visited[(state.p, state.v)] = min(strict_visited.get((state.p, state.v), inf), state.cost)

        for r in make_rotations(state):
            newv = state.v * r
            newp = state.p
            ncost = 1000 + state.cost if r != 1 else state.cost
            if strict_visited.get((newp, newv), inf) >= ncost:
                q.put_nowait(Node(ncost + estimate_cost(newp), ncost, newp, newv, state.tiles))

        newp = state.p + state.v
        if getch(newp) != "#" and strict_visited.get((newp, state.v), inf) >= (state.cost + 1):
            q.put_nowait(Node(state.cost + 1 + estimate_cost(newp), state.cost + 1, newp, state.v, state.tiles | {newp}))

        if getch(state.p) == "E" and md >= state.cost:
            md = min(md, state.cost)
            best.append(state)

    tiles = set()
    tiles.update(*map(lambda n: n.tiles, filter(lambda n: n.cost == md, best)))
    for t in tiles:
        board[int(t.imag)][int(t.real)] = "O"
    return len(tiles)

if __name__ == "__main__":
    puzzle_names = ['day16_simple_1.txt', 'day16_simple_2.txt', 'day16_full.txt']
    for puzzle in puzzle_names:
        if os.path.exists(puzzle):
            with open(puzzle, 'r') as file:
                input_str = file.read()
            print(f"Contents of {puzzle}:\n{input_str}")  # Debug print
            grid, start, end = parse_input(input_str)
            print(f"Start: {start}, End: {end}")  # Debug print
            try:
                result = reindeer_maze(grid, start, end)
                print("Lowest score:", result)
                
                result_2 = reindeer_maze_part2(grid)
                print("Number of optimal paths:", result_2)
            except ValueError as e:
                print(e)
        else:
            print(f"File {puzzle} does not exist.")
