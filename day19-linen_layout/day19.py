import os
from typing import List, Tuple, Set

def read_patterns_and_designs(file_name: str) -> Tuple[List[str], List[str]]:
    """
    Reads the patterns and designs from the given file.

    Args:
        file_name (str): The name of the file to read from.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing the list of patterns and the list of designs.
    """
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()
    
    patterns, designs = split_patterns_and_designs(lines)
    return patterns, designs

def split_patterns_and_designs(lines: List[str]) -> Tuple[List[str], List[str]]:
    """
    Splits the lines into patterns and designs.

    Args:
        lines (List[str]): The lines to split.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing the list of patterns and the list of designs.
    """
    patterns = []
    designs = []
    is_design = False
    for line in lines:
        if line.strip() == "":
            is_design = True
            continue
        if is_design:
            designs.append(line)
        else:
            patterns.extend(line.split(", "))
    
    return patterns, designs

def count_possible_designs(towel_patterns: List[str], designs: List[str]) -> int:
    """
    Counts the number of possible designs that can be constructed using the given towel patterns.

    Args:
        towel_patterns (List[str]): The list of towel patterns.
        designs (List[str]): The list of designs.

    Returns:
        int: The number of possible designs that can be constructed.
    """
    towel_set = set(towel_patterns)
    return sum(can_construct_design(design, towel_set) for design in designs)

def can_construct_design(design: str, towel_set: Set[str]) -> bool:
    """
    Checks if a design can be constructed using the given towel patterns.

    Args:
        design (str): The design to check.
        towel_set (Set[str]): The set of towel patterns.

    Returns:
        bool: True if the design can be constructed, False otherwise.
    """
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue
        for j in range(i + 1, n + 1):
            if design[i:j] in towel_set:
                dp[j] = True

    return dp[n]

def count_all_ways_to_construct_designs(towel_patterns: List[str], designs: List[str]) -> int:
    """
    Counts all the ways to construct each design using the given towel patterns.

    Args:
        towel_patterns (List[str]): The list of towel patterns.
        designs (List[str]): The list of designs.

    Returns:
        int: The total number of ways to construct all designs.
    """
    towel_set = set(towel_patterns)
    return sum(count_ways(design, towel_set) for design in designs)

def count_ways(design: str, towel_set: Set[str]) -> int:
    """
    Counts the number of ways to construct a design using the given towel patterns.

    Args:
        design (str): The design to construct.
        towel_set (Set[str]): The set of towel patterns.

    Returns:
        int: The number of ways to construct the design.
    """
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n):
        if dp[i] == 0:
            continue
        for j in range(i + 1, n + 1):
            if design[i:j] in towel_set:
                dp[j] += dp[i]

    return dp[n]

if __name__ == "__main__":
    file_names = ['day19_simple.txt', 'day19_full.txt']
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Solving for file {file_name}")
            patterns, designs = read_patterns_and_designs(file_name)
            result_part1 = count_possible_designs(patterns, designs)
            result_part2 = count_all_ways_to_construct_designs(patterns, designs)
            print("Number of possible designs (Part 1):", result_part1)
            print("Total number of ways to construct designs (Part 2):", result_part2)
        else:
            print(f"File {file_name} does not exist.")
