import graphviz
from typing import Dict, List, Tuple
from day24 import parse_input, GateType

def visualize_circuit(initial_values: Dict[str, int], gate_connections: List[Tuple[str, GateType, str, str]], output_file: str) -> None:
    """
    Visualize the circuit using graphviz.
    
    Args:
        initial_values (Dict[str, int]): The initial values of the wires.
        gate_connections (List[Tuple[str, GateType, str, str]]): The gate connections.
        output_file (str): The output file name for the visualization.
    """
    dot = graphviz.Digraph(comment='Circuit Visualization')

    # Add nodes for initial values
    for wire, value in initial_values.items():
        dot.node(wire, f'{wire}: {value}', shape='circle')

    # Add edges for gate connections
    for input1, gate, input2, output in gate_connections:
        gate_label = gate.name
        dot.edge(input1, output, label=f'{gate_label} ({input1})')
        dot.edge(input2, output, label=f'{gate_label} ({input2})')

    # Render the graph to a file
    dot.render(output_file)
    print(f"Graph rendered to {output_file}")

def main(input_file: str, output_file: str) -> None:
    """
    Main function to read input, parse it, and visualize the circuit.
    
    Args:
        input_file (str): The path to the input file.
        output_file (str): The output file name for the visualization.
    """
    with open(input_file) as f:
        initial_values, gate_connections = parse_input(f)
    
    visualize_circuit(initial_values, gate_connections, output_file)

if __name__ == '__main__':
    input_files = ["day24_simple.txt", "day24_full.txt"]
    for input_file in input_files:
        output_file = input_file.replace('.txt', '_circuit')
        main(input_file, output_file)
