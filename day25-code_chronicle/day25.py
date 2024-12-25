import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def count_fitting_pairs(locks: List[List[int]], keys: List[List[int]]) -> int:
    """
    Count the number of unique lock/key pairs that fit together without overlapping in any column.

    Args:
        locks (List[List[int]]): List of lock heights.
        keys (List[List[int]]): List of key heights.

    Returns:
        int: Number of fitting lock/key pairs.
    """
    return sum(all(lock[i] + key[i] <= 5 for i in range(len(lock))) for lock in locks for key in keys)

def process_file(file_path: str) -> None:
    """
    Process the given file to count the number of unique lock/key pairs that fit together.

    Args:
        file_path (str): Path to the file containing lock and key schematics.
    """
    logging.info(f'Processing file: {file_path}')
    locks, keys = [], []
    try:
        with open(file_path) as f:
            for lines in [block.split("\n") for block in f.read().split("\n\n")]:
                heights = list(map(sum, zip([0]*5, *[[(c == "#") for c in lines[i+1]] for i in range(5)])))
                (locks if lines[0] == "#####" else keys).append(heights)
        result = count_fitting_pairs(locks, keys)
        logging.info(f'Number of unique lock/key pairs that fit together for {file_path}: {result}')
    except FileNotFoundError:
        logging.error(f'Error: File {file_path} not found.')
    except Exception as e:
        logging.error(f'Error processing file {file_path}: {e}')

if __name__ == '__main__':
    input_files = ["day25_simple.txt", "day25_full.txt"]
    for input_file in input_files:
        process_file(input_file)
