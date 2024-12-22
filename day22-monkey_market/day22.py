import os
from collections import defaultdict
from typing import List, Tuple, Dict

def read_initial_secrets(filepath: str) -> List[int]:
    """
    Reads initial secrets from a file.

    Args:
        filepath (str): The path to the file containing the secrets.

    Returns:
        List[int]: A list of integers representing the secrets.
    """
    with open(filepath, 'r') as file:
        return [int(line.strip()) for line in file]

def mix_and_prune(secret: int, value: int) -> int:
    """
    Mixes and prunes a secret with a given value.

    Args:
        secret (int): The initial secret.
        value (int): The value to mix with the secret.

    Returns:
        int: The mixed and pruned secret.
    """
    return (secret ^ value) % 16777216

def next_secret(secret: int) -> int:
    """
    Generates the next secret based on the current secret.

    Args:
        secret (int): The current secret.

    Returns:
        int: The next secret.
    """
    secret = mix_and_prune(secret, secret << 6)
    secret = mix_and_prune(secret, secret >> 5)
    secret = mix_and_prune(secret, secret << 11)
    return secret

def p1_simulate_secrets(initial_secrets: List[int], iterations: int) -> List[int]:
    """
    Simulates the secrets for a given number of iterations.

    Args:
        initial_secrets (List[int]): The initial secrets.
        iterations (int): The number of iterations to simulate.

    Returns:
        List[int]: The final secrets after simulation.
    """
    results = []
    for secret in initial_secrets:
        for _ in range(iterations):
            secret = next_secret(secret)
        results.append(secret)
    return results

def p2_simulate_secrets(initial_secrets: List[int]) -> Tuple[int, Tuple[int, int, int, int]]:
    """
    Simulates the secrets and finds the sequence with the maximum profit.

    Args:
        initial_secrets (List[int]): The initial secrets.

    Returns:
        Tuple[int, Tuple[int, int, int, int]]: The maximum profit and the best sequence.
    """
    total: Dict[Tuple[int, int, int, int], int] = defaultdict(int)
    for secret in initial_secrets:
        seqs: Dict[Tuple[int, int, int, int], int] = dict()
        seq = (0, 0, 0, 0)
        for i in range(2000):
            prev = secret % 10
            secret = next_secret(secret)
            seq = (*seq[1:], secret % 10 - prev)
            if i >= 3 and seq not in seqs:
                seqs[seq] = secret % 10
        for s in seqs:
            total[s] += seqs[s]
    winner = sorted([(v, k) for k, v in total.items()])[-1]
    return winner

if __name__ == "__main__":
    file_names = ['day22_simple.txt','day22_full.txt']
    final_results = []
    for file_name in file_names:
        if os.path.exists(file_name):
            print(f"Processing {file_name}")
            initial_secrets = read_initial_secrets(file_name)
            iterations = 2000
            final_secrets = p1_simulate_secrets(initial_secrets, iterations)
            result_sum = sum(final_secrets)
            print(f"Part 1 result: {result_sum}")
            
            max_profit, best_sequence = p2_simulate_secrets(initial_secrets)
            print(f"Max profit: {max_profit} with sequence {best_sequence}")
        else:
            print(f"File {file_name} does not exist.")
