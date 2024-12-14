import os
import re
from itertools import count
from typing import List, Tuple

def read_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of strings, each representing a section of the input.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: List of sections from the input file.
    """
    with open(file_path, 'r') as file:
        return file.read().strip().split("\n\n")

def parse_robots(file_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Parses the robot positions and velocities from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Tuple[Tuple[int, int], Tuple[int, int]]]: List of tuples containing positions and velocities.
    """
    pattern = r'p=(.+),(.+) v=(.+),(.+)'
    with open(file_path, 'r') as f:
        return [((int(px), int(py)), (int(vx), int(vy))) for px, py, vx, vy in 
                (re.match(pattern, line).groups() for line in f.readlines())]

def get_dest(pos: Tuple[int, int], vel: Tuple[int, int], steps: int, m: int, n: int) -> Tuple[int, int]:
    """
    Calculates the destination position after a given number of steps.

    Args:
        pos (Tuple[int, int]): Initial position.
        vel (Tuple[int, int]): Velocity.
        steps (int): Number of steps.
        m (int): Width of the grid.
        n (int): Height of the grid.

    Returns:
        Tuple[int, int]: Destination position.
    """
    return ((pos[0] + vel[0] * steps) % m, (pos[1] + vel[1] * steps) % n)

def get_nbrs(pos: Tuple[int, int], m: int, n: int) -> List[Tuple[int, int]]:
    """
    Gets the neighboring positions in the grid.

    Args:
        pos (Tuple[int, int]): Current position.
        m (int): Width of the grid.
        n (int): Height of the grid.

    Returns:
        List[Tuple[int, int]]: List of neighboring positions.
    """
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [((pos[0] + dx) % m, (pos[1] + dy) % n) for dx, dy in deltas]

def contains_cluster(l: List[Tuple[int, int]], m: int, n: int) -> bool:
    """
    Checks if there is a cluster of robots that is at least a quarter of the total number of robots.

    Args:
        l (List[Tuple[int, int]]): List of robot positions.
        m (int): Width of the grid.
        n (int): Height of the grid.

    Returns:
        bool: True if there is a cluster, False otherwise.
    """
    largest_group = 0
    candidates = set(l)
    num = len(candidates)
    while candidates:
        q = [list(candidates)[0]]
        visited = {q[0]}
        while q:
            current = q.pop()
            for nbr in get_nbrs(current, m, n):
                if nbr in candidates and nbr not in visited:
                    visited.add(nbr)
                    q.append(nbr)
        largest_group = max(largest_group, len(visited))
        candidates -= visited
    return largest_group >= num // 4

def part1(robots: List[Tuple[Tuple[int, int], Tuple[int, int]]], steps: int, m: int, n: int) -> int:
    """
    Solves part 1 of the problem.

    Args:
        robots (List[Tuple[Tuple[int, int], Tuple[int, int]]]): List of robot positions and velocities.
        steps (int): Number of steps.
        m (int): Width of the grid.
        n (int): Height of the grid.

    Returns:
        int: Result of part 1.
    """
    tl, tr, bl, br = 0, 0, 0, 0
    for p, v in robots:
        dest = get_dest(p, v, steps, m, n)
        if dest[0] < m // 2:
            if dest[1] < n // 2:
                tl += 1
            elif dest[1] > n // 2:
                bl += 1
        elif dest[0] > m // 2:
            if dest[1] < n // 2:
                tr += 1
            elif dest[1] > n // 2:
                br += 1
    return tl * tr * bl * br

def part2(robots: List[Tuple[Tuple[int, int], Tuple[int, int]]], m: int, n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Solves part 2 of the problem.

    Args:
        robots (List[Tuple[Tuple[int, int], Tuple[int, int]]]): List of robot positions and velocities.
        m (int): Width of the grid.
        n (int): Height of the grid.

    Returns:
        Tuple[int, List[Tuple[int, int]]]: Number of seconds and final positions of the robots.
    """
    robot_pos = [robot[0] for robot in robots]
    for seconds in count(1):
        robot_pos = [((pos[0] + vel[0]) % m, (pos[1] + vel[1]) % n) for pos, vel in zip(robot_pos, [robot[1] for robot in robots])]
        if contains_cluster(robot_pos, m, n):
            return seconds, robot_pos

def print_grid(robot_pos: List[Tuple[int, int]], m: int, n: int) -> None:
    """
    Prints the grid with robot positions.

    Args:
        robot_pos (List[Tuple[int, int]]): List of robot positions.
        m (int): Width of the grid.
        n (int): Height of the grid.
    """
    s = set(robot_pos)
    for y in range(n):
        row = ''.join('#' if (x, y) in s else '.' for x in range(m))
        print(row)

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    file_names = ['day14_simple.txt', 'day14_full.txt']
    n, m = 103, 101
    steps = 100

    for file_name in file_names:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            print(f"Reading input from file {file_name}")
            robots = parse_robots(file_path)

            # Part 1
            result_part1 = part1(robots, steps, m, n)
            print(f"Part 1: {result_part1}")

            # Part 2
            seconds, robot_pos = part2(robots, m, n)
            print(f"Seconds: {seconds}")
            print_grid(robot_pos, m, n)
        else:
            print(f"File {file_name} does not exist.")
