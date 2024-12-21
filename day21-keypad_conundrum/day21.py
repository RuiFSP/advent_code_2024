import os
from collections import Counter
from typing import Dict, Tuple, List

Keypad = Dict[str, Tuple[int, int]]
DirectionPad = Dict[str, Tuple[int, int]]
StepCounter = Counter[Tuple[int, int, bool]]

def load_codes_from_file(file_path: str) -> List[str]:
    """
    Load codes from a file.

    Args:
        file_path (str): The path to the file containing the codes.

    Returns:
        List[str]: A list of codes.
    """
    with open(file_path) as f:
        return f.read().split("\n")

def create_keypad_mapping() -> Keypad:
    """
    Create a keypad mapping.

    Returns:
        Keypad: A dictionary mapping characters to their coordinates on the keypad.
    """
    return {char: (i % 3, i // 3) for i, char in enumerate("789456123 0A")}

def create_direction_pad_mapping() -> DirectionPad:
    """
    Create a direction pad mapping.

    Returns:
        DirectionPad: A dictionary mapping characters to their coordinates on the direction pad.
    """
    return {char: (i % 3, i // 3) for i, char in enumerate(" ^A<v>")}

def calculate_steps(keypad: Keypad, sequence: str, increment: int = 1) -> StepCounter:
    """
    Calculate the steps taken on the keypad.

    Args:
        keypad (Keypad): The keypad mapping.
        sequence (str): The string of characters representing the steps.
        increment (int, optional): The increment value for the counter. Defaults to 1.

    Returns:
        StepCounter: A counter of the steps taken.
    """
    current_x, current_y = keypad["A"]
    blank_x, blank_y = keypad[" "]
    step_counter = Counter()
    for char in sequence:
        next_x, next_y = keypad[char]
        is_blank = next_x == blank_x and current_y == blank_y or next_y == blank_y and current_x == blank_x
        step_counter[(next_x - current_x, next_y - current_y, is_blank)] += increment
        current_x, current_y = next_x, next_y
    return step_counter

def process_code_sequence(code: str, keypad: Keypad, direction_pad: DirectionPad, iterations: int) -> int:
    """
    Process a code using the keypad and direction pad.

    Args:
        code (str): The code to process.
        keypad (Keypad): The keypad mapping.
        direction_pad (DirectionPad): The direction pad mapping.
        iterations (int): The number of iterations.

    Returns:
        int: The result of processing the code.
    """
    step_counter = calculate_steps(keypad, code)
    for _ in range(iterations + 1):
        step_counter = sum((calculate_steps(direction_pad, ("<" * -x + "v" * y + "^" * -y + ">" * x)[:: -1 if is_blank else 1] + "A", step_counter[(x, y, is_blank)]) for x, y, is_blank in step_counter), Counter())
    return step_counter.total() * int(code[:3])

def process_all_codes(file_path: str, iterations: int) -> int:
    """
    Process all codes in a file.

    Args:
        file_path (str): The path to the file containing the codes.
        iterations (int): The number of iterations.

    Returns:
        int: The sum of the results of processing all codes.
    """
    codes = load_codes_from_file(file_path)
    keypad = create_keypad_mapping()
    direction_pad = create_direction_pad_mapping()
    return sum(process_code_sequence(code, keypad, direction_pad, iterations) for code in codes)

if __name__ == "__main__":
    file_names = ['day21_simple.txt', 'day21_full.txt']
    final_results = []
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Processing {file_name} for 2 iteration")
            print("\t",process_all_codes(file_name, 2))
            print(f"Processing {file_name} for 25 iteration")
            print("\t",process_all_codes(file_name, 25))
        else:
            print(f"File {file_name} does not exist.")