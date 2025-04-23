import os
import itertools
from data.nodes import locations
from data.dijkstra import dijkstra
from data.graph import graph

# Utility to export a dictionary to a .py file
def export_dict_to_py(filename, var_name, data_dict):
    with open(filename, 'w') as f:
        f.write(f"{var_name} = {{\n")
        for key, value in data_dict.items():
            if isinstance(key, tuple):
                key_str = f"({repr(key[0])}, {repr(key[1])})"
            else:
                key_str = repr(key)
            f.write(f"    {key_str}: {repr(value)},\n")
        f.write("}\n")

def generate_all_paths():
    # Analytics storage
    path_trace = {}
    edge_usage = {}
    node_visit_count = {}
    distance_matrix = {}

    # Compute all-pairs paths
    pairs = list(itertools.permutations(locations, 2))

    for start, end in pairs:
        result = dijkstra(start, end, graph)
        path = result["path"]
        distance = result["distance"]

        # Path trace
        path_trace[(start, end)] = path

        # Distance matrix
        if start not in distance_matrix:
            distance_matrix[start] = {}
        distance_matrix[start][end] = distance

        # Node visit count
        for node in path[1:-1]:  # skip start and end nodes
            node_visit_count[node] = node_visit_count.get(node, 0) + 1

        # Edge usage
        for i in range(len(path) - 1):
            edge = tuple(sorted((path[i], path[i + 1])))
            edge_usage[edge] = edge_usage.get(edge, 0) + 1

    # Create a data folder if it doesn't exist
    analytics_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_io'))
    os.makedirs(analytics_dir, exist_ok=True)

    # Export all files
    export_dict_to_py(os.path.join(analytics_dir, "path_data.py"), "path_trace", path_trace)
    export_dict_to_py(os.path.join(analytics_dir, "edge_heatmap_data.py"), "edge_usage", edge_usage)
    export_dict_to_py(os.path.join(analytics_dir, "node_heatmap_data.py"), "node_visit_count", node_visit_count)
    export_dict_to_py(os.path.join(analytics_dir, "distance_matrix.py"), "distance_matrix", distance_matrix)

    print("All analytics exported to data_io folder.")

# To Run standalone
if __name__ == "__main__":
    generate_all_paths()
