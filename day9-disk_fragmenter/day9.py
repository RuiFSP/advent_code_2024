import os
from collections import deque

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

def parse_input(data, part2):
    """
    Parses the input data and returns the positions of files and spaces.

    Args:
        data (str): The input string containing file and space counts.
        part2 (bool): A flag indicating whether to use part2 logic.

    Returns:
        tuple: A tuple containing three elements:
            - file_positions (deque): A deque of tuples representing file positions. 
              Each tuple contains (start_position, count, file_id).
            - space_positions (deque): A deque of tuples representing space positions. 
              Each tuple contains (start_position, count).
            - final_positions (list): A list representing the final positions of files and spaces. 
              File positions are represented by their file_id, and spaces are represented by None.
    """
    file_positions = deque()
    space_positions = deque()
    final_positions = []
    pos = 0
    file_id = 0

    for i, char in enumerate(data):
        if i % 2 == 0:
            count = int(char)
            if part2:
                file_positions.append((pos, count, file_id))
            for _ in range(count):
                final_positions.append(file_id)
                if not part2:
                    file_positions.append((pos, 1, file_id))
                pos += 1
            file_id += 1
        else:
            count = int(char)
            space_positions.append((pos, count))
            for _ in range(count):
                final_positions.append(None)
                pos += 1

    return file_positions, space_positions, final_positions

def rearrange_files(file_positions, space_positions, final_positions):
    """
    Rearranges files in the final_positions list based on available space.

    Args:
        file_positions (list of tuples): A list of tuples where each tuple contains
            the starting position (int), size (int), and file ID (any) of a file.
        space_positions (list of tuples): A list of tuples where each tuple contains
            the starting position (int) and size (int) of available space.
        final_positions (list): A list representing the final positions of files,
            where each element is either a file ID or None.

    Raises:
        AssertionError: If the file ID at the current position does not match the expected file ID.

    Example:
        file_positions = [(5, 3, 'file1'), (10, 2, 'file2')]
        space_positions = [(0, 5), (8, 4)]
        final_positions = [None, None, None, None, None, 'file1', 'file1', 'file1', None, None, 'file2', 'file2']
        
        rearrange_files(file_positions, space_positions, final_positions)
    """
    for pos, size, file_id in reversed(file_positions):
        for space_index, (space_pos, space_size) in enumerate(space_positions):
            if space_pos < pos and size <= space_size:
                for i in range(size):
                    assert final_positions[pos + i] == file_id, f'{final_positions[pos + i]=}'
                    final_positions[pos + i] = None
                    final_positions[space_pos + i] = file_id
                space_positions[space_index] = (space_pos + size, space_size - size)
                break

def calculate_result(final_positions):
    """
    Calculate the result based on the final positions of file IDs.

    This function iterates through the list of final positions, and for each
    non-None file ID, it adds the product of the index and the file ID to the result.

    Args:
        final_positions (list of int or None): A list where each element is either
            an integer representing a file ID or None.

    Returns:
        int: The calculated result based on the given final positions.
    """
    result = 0
    for i, file_id in enumerate(final_positions):
        if file_id is not None:
            result += i * file_id
    return result

def solve(data, part2):
    """
    Solves the disk fragmenter problem for the given input data.

    Args:
        data (str): The input data as a string.
        part2 (bool): A flag indicating whether to solve part 2 of the problem.

    Returns:
        int: The result after processing the input data.
    """
    file_positions, space_positions, final_positions = parse_input(data, part2)
    rearrange_files(file_positions, space_positions, final_positions)
    return calculate_result(final_positions)

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'day9_simple.txt')
    data = read_input(file_path)

    part1_result = solve(data, False)
    part2_result = solve(data, True)

    print(f'Part 1 simple: {part1_result}')
    print(f'Part 2 simple: {part2_result}')
    
    file_path = os.path.join(os.path.dirname(__file__), 'day9_full.txt')
    data = read_input(file_path)

    part1_result = solve(data, False)
    part2_result = solve(data, True)

    print(f'Part 1 full: {part1_result}')
    print(f'Part 2 full: {part2_result}')