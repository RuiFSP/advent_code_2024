import os
import re

def read_input(file_path: str) -> list:
    """
    Reads the input from a file and returns a list of strings, where each string
    represents a block of text separated by double newlines.

    Args:
        file_path (str): The path to the input file.

    Returns:
        list: A list of strings, each representing a block of text from the file.
    """
    with open(file_path, 'r') as file:
        return file.read().strip().split("\n\n")

def parse_machine_data(machine_data: str) -> tuple:
    """
    Parses the machine data string and extracts the coordinates for buttons A, B, and the prize.

    Args:
        machine_data (str): A string containing the machine data with coordinates for buttons A, B, and the prize.

    Returns:
        tuple: A tuple containing six integers representing the coordinates (a_x, a_y, b_x, b_y, p_x, p_y).
    """
    button_a, button_b, prize = machine_data.split("\n")
    a_x, a_y = map(int, re.findall(r"(\d+)", button_a))
    b_x, b_y = map(int, re.findall(r"(\d+)", button_b))
    p_x, p_y = map(int, re.findall(r"(\d+)", prize))
    return a_x, a_y, b_x, b_y, p_x, p_y

def calculate_tokens(a_x, a_y, b_x, b_y, p_x, p_y, conversion_error=0) -> int:
    """
    Calculate the number of tokens based on given coordinates and conversion error.

    Args:
        a_x (float): The x-coordinate of point A.
        a_y (float): The y-coordinate of point A.
        b_x (float): The x-coordinate of point B.
        b_y (float): The y-coordinate of point B.
        p_x (float): The x-coordinate of point P.
        p_y (float): The y-coordinate of point P.
        conversion_error (float, optional): The conversion error to be added to p_x and p_y. Defaults to 0.

    Returns:
        int: The calculated number of tokens. Returns 0 if the calculation does not match the expected coordinates.
    """
    p_x += conversion_error
    p_y += conversion_error

    a = round((p_y / b_y - p_x / b_x) / (a_y / b_y - a_x / b_x))
    b = round((p_x - a * a_x) / b_x)

    if a * a_x + b * b_x == p_x and a * a_y + b * b_y == p_y:
        return 3 * a + b
    return 0

def process_machine_data(machine_data: str) -> tuple:
    """
    Processes the machine data and calculates tokens for two parts.

    Args:
        machine_data (str): A string containing the machine data.

    Returns:
        tuple: A tuple containing tokens for part 1 and part 2.
    """
    a_x, a_y, b_x, b_y, p_x, p_y = parse_machine_data(machine_data)
    part1_tokens = calculate_tokens(a_x, a_y, b_x, b_y, p_x, p_y)
    part2_tokens = calculate_tokens(a_x, a_y, b_x, b_y, p_x, p_y, 10000000000000)
    return part1_tokens, part2_tokens

def process_file(file_path: str) -> tuple:
    """
    Processes the input file and returns the results for part 1 and part 2.

    Args:
        file_path (str): The path to the input file.

    Returns:
        tuple: A tuple containing the sum of part 1 results and the sum of part 2 results.
    """
    machine_data_list = read_input(file_path)
    results = [process_machine_data(data) for data in machine_data_list]
    part1_results = [result[0] for result in results if result[0]]
    part2_results = [result[1] for result in results if result[1]]
    return sum(part1_results), sum(part2_results)

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    file_names = ['day13_simple.txt', 'day13_full.txt']
    for file_name in file_names:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            print(f"Reading input from file {file_name}")
            part1_sum, part2_sum = process_file(file_path)
            print(f"Part 1: {part1_sum}")
            print(f"Part 2: {part2_sum}")
        else:
            print(f"File {file_name} does not exist.")
