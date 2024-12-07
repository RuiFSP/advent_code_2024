import os
from itertools import product
from typing import Dict, List

def parse_data(file_path: str) -> Dict[int, List[int]]:
    """
    Parses a file containing data in the format "key: value1 value2 value3 ...".

    Args:
        file_path (str): The path to the file to be parsed.

    Returns:
        Dict[int, List[int]]: A dictionary where the keys are integers and the values are lists of integers.
    """
    with open(file_path) as file:
        return {int(line.split(':')[0]): list(map(int, line.split(':')[1].split())) for line in file}

def evaluate_combinations(numbers: List[int], target: int) -> int:
    """
    Evaluates all possible combinations of operations on a list of numbers to reach a target value.
    This function takes a list of integers and a target integer. It then evaluates all possible 
    combinations of the operations '+', '*', and '||' (concatenation) between the numbers to see 
    how many combinations result in the target value.
    Args:
        numbers (List[int]): A list of integers to be combined using the operations.
        target (int): The target value to be achieved through the combinations of operations.
    Returns:
        int: The number of combinations that result in the target value.
    Example:
        >>> evaluate_combinations([1, 2, 3], 6)
        1
        >>> evaluate_combinations([1, 2, 3], 23)
        1
    """
    operators = ['+', '*', '||']
    n = len(numbers) - 1
    count = 0
    
    for ops in product(operators, repeat=n):
        current_value = numbers[0]
        for i in range(n):
            if ops[i] == '+':
                current_value += numbers[i + 1]
            elif ops[i] == '*':
                current_value *= numbers[i + 1]
            elif ops[i] == '||':
                current_value = int(str(current_value) + str(numbers[i + 1]))
        
        if current_value == target:
            count += 1
            
    return count

def calculate_total_calibration(data: Dict[int, List[int]]) -> int:
    """
    Calculate the total calibration value based on the provided data.

    This function iterates through the given dictionary, where each key is a target
    value and each value is a list of integers. For each target, it evaluates the
    combinations of numbers in the list. If the number of valid combinations is
    greater than zero, the target value is added to the total calibration.

    Args:
        data (Dict[int, List[int]]): A dictionary where keys are target integers and
                                     values are lists of integers to be evaluated.

    Returns:
        int: The total calibration value calculated by summing the target values
             that have valid combinations.
    """
    total_calibration = 0
    for target, numbers in data.items():
        if evaluate_combinations(numbers, target) > 0:
            total_calibration += target
    return total_calibration

if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(__file__), 'day7_simple.txt')
    data_dict = parse_data(data_file)
    total_calibration_result = calculate_total_calibration(data_dict)
    print("Total Calibration Result:", total_calibration_result)
