import os

def read_input(file_path):
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
    for file_name in ['day10_simple.txt', 'day10_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        data = read_input(file_path)

        part1_result = sum([int(x) for x in data.split("\n")])
        part2_result = sum([int(x) for x in data.split("\n")])
        
        
        print(f'Part 1 {file_name.split("_")[1]}: {part1_result}')
        print(f'Part 2 {file_name.split("_")[1]}: {part2_result}')