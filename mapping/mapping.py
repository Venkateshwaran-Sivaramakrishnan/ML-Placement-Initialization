from extractor import DesignParser

def get_node_geometry(parser, node_id):
    """
    Given a node ID, return its position and size info from the design.
    Works for both I/O pins and cell instances.
    """
    if node_id in parser.io_pins:
        pin = parser.io_pins[node_id]
        return {
            "type": pin["type"],
            "x": pin["x"],
            "y": pin["y"],
            "width": 0,
            "height": 0,
            "is_macro": False,
            "is_fixed": True
        }
    elif node_id in parser.instances:
        inst = parser.instances[node_id]
        return {
            "x": inst["x"],
            "y": inst["y"],
            "width": inst["width"],
            "height": inst["height"],
            "is_macro": inst["is_macro"],
            "is_fixed": inst["is_fixed"],
            "cell_name": inst["cell_name"]
        }
    else:
        raise ValueError(f"Node ID {node_id} not found in design.")

# --------------------
# Example usage
# --------------------
if __name__ == "__main__":
    filepath = "ibex_nangate45.txt"  # Update path if needed
    parser = DesignParser(filepath)

    # Example: query geometry for a specific node
    node_id = 0  # Change this to a valid node ID
    geometry = get_node_geometry(parser, node_id)
    print(f"Geometry for node {node_id}:\n{geometry}")
