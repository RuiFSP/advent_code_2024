import os

def read_input(file_path: str) -> list:
    """
    Reads the content of a file and returns it as a list of strings.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: The content of the file as a list of strings.
    """
    with open(file_path, 'r') as file:
        return file.read().strip().split("\n")


if __name__ == "__main__":
    for file_name in ['day13_simple.txt', 'day13_full.txt']:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path):
            print(f"Reading input from file {file_name}")
            input_data = read_input(file_path)
            print(input_data)        
        else:
            print(f"File {file_name} does not exist.")
            