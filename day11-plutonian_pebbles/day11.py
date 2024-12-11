import os
from pathlib import Path

def read_input(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a stripped string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file with leading and trailing whitespace removed.
    """
    with open(file_path) as file:
        return file.read().strip()



if __name__ == "__main__":
    for file_name in ['day11_simple.txt', 'day11_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        input = read_input(file_path)
        
        print(f'Part 1 {file_name.split("_")[1]}: {input}')
        print(f'Part 2 {file_name.split("_")[1]}: {input}')