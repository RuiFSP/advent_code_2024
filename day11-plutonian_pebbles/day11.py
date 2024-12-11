from collections import defaultdict
import os

def read_input(file_path: str) -> list:
    """
    Reads the content of a file and returns it as a list of integers.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: The content of the file as a list of integers.
    """
    with open(file_path, 'r') as file:
        return list(map(int, file.read().strip().split()))

def apply_rules(number):
    """
    Apply specific rules to the input number and return the result.
    The function applies the following rules:
    1. If the number is in the cache, return the cached result.
    2. If the number is 0, return a list containing 1.
    3. If the number has an even number of digits, split the number into two halves and return them as a list.
    4. If the number has an odd number of digits, multiply the number by 2024 and return the result in a list.
    Args:
        number (int): The input number to which the rules are applied.
    Returns:
        list: The result after applying the rules to the input number.
    """
    if not hasattr(apply_rules, "rule_cache"):
        apply_rules.rule_cache = {}
    
    if number in apply_rules.rule_cache:
        return apply_rules.rule_cache[number]
    if number == 0:
        result = [1]
    elif len(str(number)) % 2 == 0:
        number_str = str(number)
        half_len = len(number_str) // 2
        result = [int(number_str[:half_len]), int(number_str[half_len:])]
    else:
        result = [number * 2024]
    apply_rules.rule_cache[number] = result
    return result

def process_blinks(initial_states, blink_count):
    """
    Simulates a series of blinks and processes the state transitions.

    Args:
        initial_states (list): A list of initial states represented by integers.
        blink_count (int): The number of blinks to simulate.

    Returns:
        int: The total count of all states after processing the blinks.
    """
    current_state_counts = defaultdict(int, {state: initial_states.count(state) for state in initial_states})

    for _ in range(blink_count):
        next_state_counts = defaultdict(int)
        for state, count in current_state_counts.items():
            for new_state in apply_rules(state):
                next_state_counts[new_state] += count
        current_state_counts = next_state_counts

    return sum(current_state_counts.values())

if __name__ == "__main__":
    for file_name in ['day11_simple.txt', 'day11_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path):
            initial_states = read_input(file_path)
        else:
            print(f"File {file_name} does not exist.")
            continue
        
        print(f'Q1 {file_name.split("_")[1]}: {process_blinks(initial_states, 25)}')
        print(f'Q2 {file_name.split("_")[1]}: {process_blinks(initial_states, 75)}')