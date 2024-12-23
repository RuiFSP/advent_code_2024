import os
from collections import defaultdict
from typing import List, Tuple, Dict, Set

def parse_connections(file_path: str) -> Dict[str, List[str]]:
    """
    Parses a file containing connections between nodes and returns a dictionary
    where each key is a node and the value is a list of nodes it is connected to.

    Args:
        file_path (str): The path to the file containing the connections.

    Returns:
        Dict[str, List[str]]: A dictionary of connections.
    """
    connections = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            a, b = line.strip().split('-')
            connections[a].append(b)
            connections[b].append(a)
    return connections

def find_triangles(connections: Dict[str, List[str]]) -> List[Tuple[str, str, str]]:
    """
    Finds all triangles in the connections. A triangle is a set of three nodes
    where each node is connected to the other two.

    Args:
        connections (Dict[str, List[str]]): A dictionary of connections.

    Returns:
        List[Tuple[str, str, str]]: A list of triangles.
    """
    triangles = []
    for a in connections:
        for b in connections[a]:
            for c in connections[b]:
                if c in connections[a] and a < b < c:
                    triangles.append((a, b, c))
    return triangles

def count_triangles_with_t(triangles: List[Tuple[str, str, str]]) -> int:
    """
    Counts how many triangles contain at least one node that starts with the letter 't'.

    Args:
        triangles (List[Tuple[str, str, str]]): A list of triangles.

    Returns:
        int: The number of triangles containing at least one 't' node.
    """
    return sum(1 for triangle in triangles if any(node.startswith('t') for node in triangle))

def find_cliques(connections: Dict[str, List[str]]) -> List[Set[str]]:
    """
    Finds all cliques in the connections using the Bron-Kerbosch algorithm.
    A clique is a subset of nodes where every two nodes are connected.

    Args:
        connections (Dict[str, List[str]]): A dictionary of connections.

    Returns:
        List[Set[str]]: A list of cliques.
    """
    def bron_kerbosch(R: Set[str], P: Set[str], X: Set[str], cliques: List[Set[str]]):
        if not P and not X:
            cliques.append(R)
            return
        for v in list(P):
            bron_kerbosch(R.union([v]), P.intersection(connections[v]), X.intersection(connections[v]), cliques)
            P.remove(v)
            X.add(v)

    cliques = []
    bron_kerbosch(set(), set(connections.keys()), set(), cliques)
    return cliques

def find_largest_clique(cliques: List[Set[str]]) -> Set[str]:
    """
    Finds the largest clique from a list of cliques.

    Args:
        cliques (List[Set[str]]): A list of cliques.

    Returns:
        Set[str]: The largest clique.
    """
    return max(cliques, key=len) if cliques else set()

def generate_password(clique: Set[str]) -> str:
    """
    Generates a password by joining the sorted nodes of the largest clique with commas.

    Args:
        clique (Set[str]): The largest clique.

    Returns:
        str: The generated password.
    """
    return ','.join(sorted(clique))

if __name__ == "__main__":
    file_names = ['day23_simple.txt', 'day23_full.txt']
    final_results = []
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Processing {file_name}")
            connections = parse_connections(file_name)
            triangles = find_triangles(connections)
            count = count_triangles_with_t(triangles)
            cliques = find_cliques(connections)
            largest_clique = find_largest_clique(cliques)
            password = generate_password(largest_clique)
            final_results.append((file_name, count, password))
        else:
            print(f"File {file_name} does not exist.")
    
    for file_name, count, password in final_results:
        print(f"{file_name}: {count} triangles with at least one 't', LAN party password: {password}")