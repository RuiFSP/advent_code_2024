import re
import os
from typing import List, Tuple

def load_program(filename: str) -> List[int]:
    """
    Load the program from a file.

    Args:
        filename (str): The name of the file to load the program from.

    Returns:
        List[int]: The program as a list of integers.
    """
    with open(filename) as f:
        return list(map(int, re.findall(r'\d+', f.read())))

def execute_instruction(prog: List[int], a: int, b: int, c: int, i: int, R: List[int]) -> Tuple[int, int, int, int, List[int]]:
    """
    Execute a single instruction from the program.

    Args:
        prog (List[int]): The program as a list of integers.
        a (int): The value of register a.
        b (int): The value of register b.
        c (int): The value of register c.
        i (int): The current instruction index.
        R (List[int]): The result list.

    Returns:
        Tuple[int, int, int, int, List[int]]: The updated values of a, b, c, i, and R.
    """
    C = {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}
    op = prog[i + 1]
    match prog[i]:
        case 0: a = a >> C[op]
        case 1: b = b ^ op
        case 2: b = 7 & C[op]
        case 3: i = op - 2 if a else i
        case 4: b = b ^ c
        case 5: R.append(C[op] & 7)
        case 6: b = a >> C[op]
        case 7: c = a >> C[op]
    return a, b, c, i + 2, R

def eval_program(a: int, b: int, c: int, prog: List[int]) -> List[int]:
    """
    Evaluate the entire program.

    Args:
        a (int): The initial value of register a.
        b (int): The initial value of register b.
        c (int): The initial value of register c.
        prog (List[int]): The program as a list of integers.

    Returns:
        List[int]: The result list after evaluating the program.
    """
    i = 0
    R = []
    while i in range(len(prog)):
        a, b, c, i, R = execute_instruction(prog, a, b, c, i, R)
    return R

def find_solution(a: int, b: int, c: int, prog: List[int], i: int = 0) -> None:
    """
    Find a solution by recursively evaluating the program.

    Args:
        a (int): The initial value of register a.
        b (int): The initial value of register b.
        c (int): The initial value of register c.
        prog (List[int]): The program as a list of integers.
        i (int, optional): The current depth of recursion. Defaults to 0.
    """
    if eval_program(a, b, c, prog) == prog:
        print(a)
    if eval_program(a, b, c, prog) == prog[-i:] or not i:
        for n in range(8):
            find_solution(8 * a + n, b, c, prog, i + 1)

if __name__ == "__main__":
    file_names = ['day17_simple.txt', 'day17_full.txt']
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Solving for file {file_name}")
            a, b, c, *prog = load_program(file_name)
            print(*eval_program(a, b, c, prog), sep=',')
            find_solution(0, b, c, prog)
        else:
            print(f"File {file_name} does not exist.")
