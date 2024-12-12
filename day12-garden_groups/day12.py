import os

def read_input(file_path: str) -> list:
    """
    Reads the content of a file and returns it as a list of strings.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: The content of the file as a list of strings.
    """
    with open(file_path, 'r') as file:
        return file.read().strip().split("\n")

def create_graph(lines: list) -> dict:
    """
    Creates a graph representation from the input lines.

    Args:
        lines (list): The input lines.

    Returns:
        dict: The graph representation.
    """
    rows, cols = len(lines), len(lines[0])
    graph = {complex(row, col): char for row, line in enumerate(lines) for col, char in enumerate(line)}
    for row in range(-1, rows + 1):
        graph[complex(row, -1)] = graph[complex(row, cols)] = "#"
    for col in range(-1, cols + 1):
        graph[complex(-1, col)] = graph[complex(rows, col)] = "#"
    return graph

def explore_region(visited, node, color, direction, graph):
    """
    Explores a region in the graph using DFS.

    Args:
        visited (set): The set of visited nodes.
        node (complex): The current node.
        color (str): The color of the region.
        direction (complex): The current direction.
        graph (dict): The graph representation.

    Returns:
        tuple: The area, perimeter, and sides of the region.
    """
    if graph[node] != color:
        if graph[node + direction * 1j] == color or graph[node - direction + direction * 1j] != color:
            return 0, 1, 1
        else:
            return 0, 1, 0
    if node in visited:
        return 0, 0, 0
    visited.add(node)
    area, perimeter, sides = 1, 0, 0
    for d in (1, -1, 1j, -1j):
        a, p, s = explore_region(visited, node + d, color, d, graph)
        area += a
        perimeter += p
        sides += s
    return area, perimeter, sides

def process_file(file_path):
    """
    Processes the input file and calculates the answers for Q1 and Q2.

    Args:
        file_path (str): The path to the input file.
    """
    lines = read_input(file_path)
    graph = create_graph(lines)
    visited = set()
    total_area_perimeter, total_area_sides = 0, 0
    for node in graph:
        if node not in visited and graph[node] != "#":
            area, perimeter, sides = explore_region(visited, node, graph[node], 1, graph)
            total_area_perimeter += area * perimeter
            total_area_sides += area * sides
    print(f'Q1 {os.path.basename(file_path).split("_")[1]}: {total_area_perimeter}')
    print(f'Q2 {os.path.basename(file_path).split("_")[1]}: {total_area_sides}')

if __name__ == "__main__":
    for file_name in ['day12_simple.txt', 'day12_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print(f"File {file_name} does not exist.")