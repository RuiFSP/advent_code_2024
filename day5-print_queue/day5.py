import os
from typing import List, Tuple

def read_page_ordering(file_path: str) -> List[Tuple[int, int]]:
    """
    Reads a file containing page ordering information and returns a list of tuples.

    Each line in the file should contain two integers separated by a pipe ('|') character,
    representing the current page and the next page. The function stops reading when it
    encounters an empty line.

    Args:
        file_path (str): The path to the file containing the page ordering information.

    Returns:
        List[Tuple[int, int]]: A list of tuples where each tuple contains two integers
        representing the current page and the next page.
    """
    page_ordering = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                break
            page, next_page = map(int, line.strip().split("|"))
            page_ordering.append((page, next_page))
    return page_ordering

def get_rules_and_safety_manuals(file_path: str):
    """
    Reads the page ordering and safety manuals from the given file.

    The function first reads the page ordering using the `read_page_ordering` function.
    Then, it reads the safety manuals from the file, skipping initial lines until an empty line is encountered.
    Each subsequent line is split by commas and converted to a list of integers.

    Args:
        file_path (str): The path to the file containing the page ordering and safety manuals.

    Returns:
        tuple: A tuple containing:
            - page_ordering: The page ordering data as returned by `read_page_ordering`.
            - safety_manuals (list of list of int): A list of safety manuals, where each manual is represented as a list of integers.
    """
    page_ordering = read_page_ordering(file_path)
    safety_manuals = []
    with open(file_path, 'r') as file:
        skip_lines = True
        for line in file:
            if skip_lines:
                if line.strip() == "":
                    skip_lines = False
                continue
            safety_manuals.append(list(map(int, line.strip().split(','))))
    return page_ordering, safety_manuals

def compare_pages(page1: int, page2: int, rules: List[Tuple[int, int]]) -> int:
    """
    Compare two pages based on a set of rules.

    Args:
        page1 (int): The first page number to compare.
        page2 (int): The second page number to compare.
        rules (List[Tuple[int, int]]): A list of tuples representing the rules. 
                                       Each tuple contains two integers where the first integer 
                                       should come before the second integer.

    Returns:
        int: Returns -1 if page1 should come before page2 according to the rules,
             1 if page2 should come before page1 according to the rules,
             and 0 if there is no rule dictating the order between page1 and page2.
    """
    rules_dict = {rule: -1 for rule in rules}
    if (page1, page2) in rules_dict:
        return -1
    elif (page2, page1) in rules_dict:
        return 1
    return 0

def sort_pages(pages: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    """
    Sorts a list of pages based on custom rules.

    Args:
        pages (List[int]): A list of page numbers to be sorted.
        rules (List[Tuple[int, int]]): A list of tuples where each tuple contains two integers representing a custom sorting rule.

    Returns:
        List[int]: The sorted list of page numbers.
    """
    return sorted(pages, key=lambda page: [compare_pages(page, other, rules) for other in pages])

def process_manuals(safety_manuals: List[List[int]], page_ordering: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Processes a list of safety manuals and determines which manuals are safe and which are unsafe based on a given page ordering.
    Args:
        safety_manuals (List[List[int]]): A list of safety manuals, where each manual is represented as a list of page numbers.
        page_ordering (List[Tuple[int, int]]): A list of tuples representing the correct page ordering. Each tuple contains two integers representing the page numbers that should be in order.
    Returns:
        Tuple[int, int]: A tuple containing two integers:
            - The sum of the middle page numbers of all manuals marked as safe.
            - The sum of the middle page numbers of all manuals marked as unsafe.
    """
    manuals_marked_safe = []
    manuals_marked_unsafe = []
    for manual in safety_manuals:
        sorted_manual = sort_pages(manual, page_ordering)
        if manual == sorted_manual:
            manuals_marked_safe.append(manual)
        else:
            manuals_marked_unsafe.append(sorted_manual)
    
    safe_total = sum(manual[len(manual) // 2] for manual in manuals_marked_safe)
    unsafe_total = sum(manual[len(manual) // 2] for manual in manuals_marked_unsafe)
    return safe_total, unsafe_total

if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), "day5-print_queue", "day5_full_1.txt")
    page_ordering, safety_manuals = get_rules_and_safety_manuals(file_path)
    safe_total, unsafe_total = process_manuals(safety_manuals, page_ordering)
    print("Part1 total: ", safe_total)
    print("Part2 total: ", unsafe_total)
