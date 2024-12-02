import os
from typing import Tuple, List


def read_lists_from_file(filepath: str) -> Tuple[List[int], List[int]]:
    """
    Reads two lists of integers from a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        tuple: Two lists of integers.
    """
    list_1 = []
    list_2 = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                values = line.split()
                list_1.append(int(values[0]))
                list_2.append(int(values[1]))
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except ValueError:
        print(f"Invalid value in file: {filepath}")
    return list_1, list_2

def total_distance(list_1: List[int], list_2: List[int]) -> int:
    """
    Calculates the total distance between two lists of integers.

    Args:
        list_1 (list): The first list of integers.
        list_2 (list): The second list of integers.

    Returns:
        int: The total distance between the two lists.
    """
    sorted_list_1 = sorted(list_1)
    sorted_list_2 = sorted(list_2)
    
    return sum(abs(num1 - num2) for num1, num2 in zip(sorted_list_1, sorted_list_2))

def total_similarity(list_1: List[int], list_2: List[int]) -> int:
    """
    Calculates the total similarity between two lists of integers.

    Args:
        list_1 (list): The first list of integers.
        list_2 (list): The second list of integers.

    Returns:
        int: The total similarity between the two lists.
    """
    sorted_list_1 = sorted(list_1)
    sorted_list_2 = sorted(list_2)

    count_dict = {}
    for num in sorted_list_2:
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1

    total_similarity = sum(num1 * count_dict.get(num1, 0) for num1 in sorted_list_1)
    
    return total_similarity

if __name__ == "__main__":
    list_1, list_2 = read_lists_from_file(os.path.join(os.path.dirname(__file__), 'day1_simple_1.txt'))
    print(total_distance(list_1, list_2))    
    list_3, list_4 = read_lists_from_file(os.path.join(os.path.dirname(__file__), 'day1_full_1.txt'))
    print(total_distance(list_3, list_4))
    list_5, list_6 = read_lists_from_file(os.path.join(os.path.dirname(__file__), 'day1_simple_2.txt'))
    print(total_similarity(list_5, list_6))
    list_1, list_2 = read_lists_from_file(os.path.join(os.path.dirname(__file__), 'day1_full_2.txt'))
    print(total_similarity(list_1, list_2))
