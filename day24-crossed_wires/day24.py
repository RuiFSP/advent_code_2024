import logging
from typing import Iterator, NamedTuple, Dict, List, Tuple, Union, Iterator
from enum import Enum, auto

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GateType(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()

class GateOperation(NamedTuple):
    label: str
    position: int

class GateMismatch(NamedTuple):
    expr1: Union["GateOperation", "GateMismatch"]
    expr2: Union["GateOperation", "GateMismatch"]
    gate: GateType
    position: int

def parse_input(lines: Iterator[str]) -> Tuple[Dict[str, int], List[Tuple[str, GateType, str, str]]]:
    """
    Parse the input lines into initial values and gate connections.
    
    Args:
        lines (Iterator[str]): The input lines.
    
    Returns:
        Tuple[Dict[str, int], List[Tuple[str, GateType, str, str]]]: A tuple containing the initial values and gate connections.
    """
    initial_values = {}
    gate_connections = []
    part = 1
    for line in lines:
        line = line.strip()
        if line == "":
            part = 2
            continue
        if part == 1:
            wire, value = line.split(": ")
            initial_values[wire] = int(value)
        else:
            input1, gate, input2, _, output = line.split()
            gate_connections.append((input1, GateType[gate], input2, output))
    logging.debug(f"Parsed initial values: {initial_values}")
    logging.debug(f"Parsed gate connections: {gate_connections}")
    return initial_values, gate_connections

def simulate_gates(initial_values: Dict[str, int], gate_connections: List[Tuple[str, GateType, str, str]]) -> Dict[str, int]:
    """
    Simulate the gates based on initial values and gate connections.
    
    Args:
        initial_values (Dict[str, int]): The initial values of the wires.
        gate_connections (List[Tuple[str, GateType, str, str]]): The gate connections.
    
    Returns:
        Dict[str, int]: The current values of the wires after simulation.
    """
    current_values = initial_values.copy()
    pending_outputs = {output for _, _, _, output in gate_connections if output.startswith("z")}
    logging.info(f"Starting gate simulation with pending outputs: {pending_outputs}")
    while pending_outputs:
        for input1, gate, input2, output in gate_connections:
            if input1 in current_values and input2 in current_values:
                result = evaluate_gate(gate, current_values[input1], current_values[input2])
                current_values[output] = result
                logging.debug(f"Evaluated gate {gate} with inputs {input1}={current_values[input1]}, {input2}={current_values[input2]} -> {output}={result}")
                if output in pending_outputs:
                    pending_outputs.remove(output)
    logging.info(f"Completed gate simulation with final values: {current_values}")
    return current_values

def evaluate_gate(gate: GateType, value1: int, value2: int) -> int:
    """
    Evaluate the result of a gate operation.
    
    Args:
        gate (GateType): The type of gate.
        value1 (int): The first input value.
        value2 (int): The second input value.
    
    Returns:
        int: The result of the gate operation.
    """
    if gate == GateType.AND:
        return value1 & value2
    elif gate == GateType.OR:
        return value1 | value2
    elif gate == GateType.XOR:
        return value1 ^ value2
    else:
        raise ValueError(f"Unknown gate: {gate}")

def get_output_value(current_values: Dict[str, int]) -> int:
    """
    Calculate the output value from the current values of the wires.
    
    Args:
        current_values (Dict[str, int]): The current values of the wires.
    
    Returns:
        int: The output value.
    """
    result = 0
    for wire, value in current_values.items():
        if value and wire.startswith("z"):
            position = int(wire[1:])
            result += 1 << position
    logging.debug(f"Calculated output value: {result}")
    return result

def find_swaps(gate_connections: List[Tuple[str, GateType, str, str]]) -> Iterator[Tuple[str, str]]:
    """
    Find and yield swaps in the gate connections.
    
    Args:
        gate_connections (List[Tuple[str, GateType, str, str]]): The gate connections.
    
    Yields:
        Iterator[Tuple[str, str]]: The swaps found.
    """
    while True:
        swap = find_swap(gate_connections)
        if swap:
            logging.info(f"Found swap: {swap}")
            yield swap
            swap_outputs(swap[0], swap[1], gate_connections)
        else:
            break

def find_swap(gate_connections: List[Tuple[str, GateType, str, str]]) -> Union[Tuple[str, str], None]:
    """
    Find a single swap in the gate connections.
    
    Args:
        gate_connections (List[Tuple[str, GateType, str, str]]): The gate connections.
    
    Returns:
        Union[Tuple[str, str], None]: The swap found, or None if no swap is found.
    """
    gates_by_output = {output: (input1, gate, input2) for input1, gate, input2, output in gate_connections}
    expressions = {get_expr(output, gates_by_output): output for output in gates_by_output}
    for expr, output in expressions.items():
        expr = get_expr(output, gates_by_output)
        if expr.position == -1 and output.startswith("z"):
            expr1, expr2, gate, _ = expr
            position = int(output[1:])
            if gate == GateType.XOR:
                input1, _, input2 = gates_by_output[output]
                other_input = {expr: wire for expr, wire in zip((expr1, expr2), (input2, input1))}
                if GateOperation("Carry", position) in (expr1, expr2):
                    return (
                        other_input[GateOperation("Carry", position)],
                        expressions[GateOperation("Xor", position)],
                    )
                if GateOperation("Xor", position) in (expr1, expr2):
                    return (
                        other_input[GateOperation("Xor", position)],
                        expressions[GateOperation("Carry", position)],
                    )
        elif expr.position < 0:
            continue
        elif expr.label == "Digit" and output != f"z{expr.position:02d}":
            return output, f"z{expr.position:02d}"
    return None

def get_expr(output: str, gates_by_output: Dict[str, Tuple[str, GateType, str]]) -> Union[GateOperation, GateMismatch]:
    """
    Get the expression for a given output.
    
    Args:
        output (str): The output wire.
        gates_by_output (Dict[str, Tuple[str, GateType, str]]): The gates by output.
    
    Returns:
        Union[GateOperation, GateMismatch]: The expression for the output.
    """
    if output[0] in "xy":
        return GateOperation(output[0], int(output[1:]))
    input1, gate, input2 = gates_by_output[output]
    expr1 = get_expr(input1, gates_by_output)
    expr2 = get_expr(input2, gates_by_output)
    if isinstance(expr1, GateMismatch) or isinstance(expr2, GateMismatch):
        return GateMismatch(expr1, expr2, gate, -2)
    if expr1.position == expr2.position:
        labels = {expr1.label, expr2.label}
        if labels == {"x", "y"}:
            if gate == GateType.XOR:
                return GateOperation("Xor" if expr1.position > 0 else "Digit", expr1.position)
            elif gate == GateType.AND:
                if expr1.position == 0:
                    return GateOperation("Carry", 1)
                else:
                    return GateOperation("And", expr1.position)
        if labels == {"Carry", "Xor"} and gate in (GateType.AND, GateType.XOR):
            return GateOperation("Partial" if gate == GateType.AND else "Digit", expr1.position)
        if labels == {"Partial", "And"} and gate == GateType.OR:
            return GateOperation("Carry", expr1.position + 1)
    if expr1.position < 0 or expr2.position < 0:
        return GateMismatch(expr1, expr2, gate, -2)
    return GateMismatch(expr1, expr2, gate, -1)

def swap_outputs(output1: str, output2: str, gate_connections: List[Tuple[str, GateType, str, str]]) -> None:
    """
    Swap the outputs in the gate connections.
    
    Args:
        output1 (str): The first output wire.
        output2 (str): The second output wire.
        gate_connections (List[Tuple[str, GateType, str, str]]): The gate connections.
    """
    for i, (input1, gate, input2, output) in enumerate(gate_connections):
        if output == output1:
            new_output = output2
        elif output == output2:
            new_output = output1
        else:
            new_output = output
        gate_connections[i] = (input1, gate, input2, new_output)

def process_file(input_file: str) -> None:
    """
    Process a single input file to read input, simulate gates, and find swaps.
    
    Args:
        input_file (str): The path to the input file.
    """
    with open(input_file) as f:
        initial_values, gate_connections = parse_input(f)
    logging.info(f"Processing file: {input_file}")
    
    output_value = get_output_value(simulate_gates(initial_values, gate_connections))
    logging.info(f"Output value for {input_file}: {output_value}")
    print(f"Output value for {input_file}: {output_value}")
    
    swaps = list(find_swaps(gate_connections))
    if len(swaps) < 4:
        logging.warning(f"Not enough swaps found for {input_file}")
        print(f"Not enough swaps found for {input_file}\n")
    else:
        swap1, swap2, swap3, swap4 = swaps[:4]
        sorted_swaps = sorted(swap1 + swap2 + swap3 + swap4)
        logging.info(f"Swaps found for {input_file}: {sorted_swaps}")
        print(f"Swaps found for {input_file}: {','.join(sorted_swaps)}\n")


if __name__ == '__main__':
    input_files = ["day24_simple.txt", "day24_full.txt"]
    for input_file in input_files:
        process_file(input_file)