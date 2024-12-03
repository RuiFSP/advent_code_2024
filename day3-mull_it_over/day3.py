import os
from typing import List
import re
import logging

logging.basicConfig(level=logging.INFO, force=True)

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
        logging.error(f"File not found: {filepath}")
        return []

def parse_lines(lines: List[str]) -> int:
    """
    Parses lines to find patterns of 'mul(x,y)' and calculates the sum of their products.

    Args:
        lines (List[str]): The list of lines to parse.

    Returns:
        int: The sum of the products of the matched patterns.
    """
    pattern = r"mul\((\d+),(\d+)\)"
    total_sum = 0

    for line in lines:
        print(f"Line: {line}")  # Debug print
        for match in re.finditer(pattern, line):
            x, y = match.groups()
            total_sum += int(x) * int(y)

    return total_sum

def parse_lines_do_dont(lines: List[str]) -> int:
    pattern = r"mul\((\d+),(\d+)\)"
    total_sum = 0

    for line in lines:
        print(f"Line: {line}")

        # Split line into parts from start to "don't()", then from "don't()" to "do()", and repeat the process until we reach the end of the line
        parts = re.split(r"(don't\(\)|do\(\))", line)
        print(f"Parts: {parts}")

        valid = True
        for part in parts:
            if part == "don't()":
                valid = False
            elif part == "do()":
                valid = True
            elif valid:
                print(f"Valid Part: {part}")
                for match in re.finditer(pattern, part):
                    x, y = match.groups()
                    total_sum += int(x) * int(y)

    return total_sum


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "day3_full_2.txt")
    lines = read_lines_from_file(filepath)
    result = parse_lines_do_dont(lines)
    print(f"Result: {result}")
