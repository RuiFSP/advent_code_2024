import os
from typing import List

def read_lines_from_file(filepath: str) -> List[str]:
    """
    Reads lines from a file and returns them as a list of strings.

    Args:
        filepath (str): The path to the file to read.

    Returns:
        List[str]: The list of lines from the file.
    """
    try:
        with open(filepath, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []

def parse_line_to_integers(line: str) -> List[int]:
    """
    Parses a line of space-separated integers.

    Args:
        line (str): The line to parse.

    Returns:
        List[int]: The list of integers parsed from the line.
    """
    try:
        return [int(value) for value in line.split()]
    except ValueError:
        print(f"Invalid value in line: {line.strip()}")
        return []

def is_strictly_increasing_or_decreasing(values: List[int]) -> bool:
    return (all(values[i] < values[i+1] for i in range(len(values)-1)) or 
            all(values[i] > values[i+1] for i in range(len(values)-1)))

def has_valid_differences(values: List[int], tolerance: int = 4) -> bool:
    return all(abs(values[i] - values[i+1]) < tolerance for i in range(len(values)-1))

def is_safe_report(values: List[int], tolerance: int = 4) -> bool:
    if is_strictly_increasing_or_decreasing(values) and has_valid_differences(values, tolerance):
        return True
    for i in range(len(values)):
        modified_values = values[:i] + values[i+1:]
        if is_strictly_increasing_or_decreasing(modified_values) and has_valid_differences(modified_values, tolerance):
            return True
    return False

def count_safe_reports(filepath: str, tolerance: int = 4) -> int:
    """
    Counts the number of safe reports in a file.

    Args:
        filepath (str): The path to the file to read.
        tolerance (int): The tolerance for valid differences.

    Returns:
        int: The count of safe reports.
    """
    lines = read_lines_from_file(filepath)
    counter = 0
    for line in lines:
        values = parse_line_to_integers(line)
        if values and is_safe_report(values, tolerance):
            counter += 1
    return counter

if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), 'day2_full_1.txt')
    safe_reports = count_safe_reports(filepath)
    print(f"Safe reports: {safe_reports}")
