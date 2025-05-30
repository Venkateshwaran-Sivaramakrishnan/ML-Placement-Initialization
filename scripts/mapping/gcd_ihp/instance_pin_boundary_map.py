import json
from extractor import DesignParser
import numpy as np

# Mapping from boundary to boxes
BOUNDARY_BOXES = {
    "NORTH":     [0.25, 0.5, 0.75, 1],
    "NORTHEAST": [0, 0.5, 0.5, 1],
    "EAST":      [0, 0.25, 0.5, 0.75],
    "SOUTHEAST": [0, 0, 0.5, 0.5],
    "SOUTH":     [0.25, 0, 0.75, 0.5],
    "SOUTHWEST": [0.5, 0, 1, 0.5],
    "WEST":      [0.5, 0.25, 1, 0.75],
    "NORTHWEST": [0.5, 0.5, 1, 1],
    "INTERNAL":  [0, 0, 0, 0]
}

def get_boundary(x, y, core):
    lx, ly, ux, uy = core["lx"], core["ly"], core["ux"], core["uy"]
    if x < lx and y > uy:
        return "NORTHWEST"
    elif x > ux and y > uy:
        return "NORTHEAST"
    elif x < lx and y < ly:
        return "SOUTHWEST"
    elif x > ux and y < ly:
        return "SOUTHEAST"
    elif y > uy:
        return "NORTH"
    elif y < ly:
        return "SOUTH"
    elif x < lx:
        return "WEST"
    elif x > ux:
        return "EAST"
    else:
        return "INTERNAL"

def main(design_txt):
    parser = DesignParser(design_txt)
    core = parser.design_info["core_region"]

    # Precompute pin boundaries and boxes
    pin_boundaries = {}
    pin_boxes = {}
    for pin_id, pin in parser.io_pins.items():
        x, y = pin["x"], pin["y"]
        boundary = get_boundary(x, y, core)
        pin_boundaries[pin_id] = boundary
        pin_boxes[pin_id] = BOUNDARY_BOXES.get(boundary, [0, 0, 0, 0])

    # For each instance, find connected pins and their boundaries/boxes
    node_map = {}
    for node_id in parser.instances.keys():
        connected_pins = []
        for net_id, nodes in parser.hypergraph.items():
            if node_id == net_id or node_id in nodes:
                for pin_id in parser.io_pins:
                    if pin_id == net_id or pin_id in nodes:
                        pin = parser.io_pins[pin_id]
                        connected_pins.append({
                            "pin_id": pin_id,
                            "name": pin["name"],
                            "type": pin["type"],
                            "boundary": pin_boundaries[pin_id],
                            "boxes": pin_boxes[pin_id]
                        })
        # Remove duplicates
        unique_pins = {p["pin_id"]: p for p in connected_pins}
        if unique_pins:
            node_map[node_id] = list(unique_pins.values())
        else:
            # Mark as unconnected
            node_map[node_id] = [{
                "pin_id": None,
                "name": None,
                "type": None,
                "boundary": "UNCONNECTED",
                "boxes": [0, 0, 0, 0]
            }]

    # Now add all pins (even those not connected to any instance)
    all_pin_ids = set(parser.io_pins.keys())
    all_connected_pins = set()
    for pins in node_map.values():
        all_connected_pins.update(p["pin_id"] for p in pins if p["pin_id"] is not None)
    unconnected_pins = all_pin_ids - all_connected_pins

    for pin_id in unconnected_pins:
        pin = parser.io_pins[pin_id]
        node_map[f"PIN_{pin_id}"] = [{
            "pin_id": pin_id,
            "name": pin["name"],
            "type": pin["type"],
            "boundary": pin_boundaries[pin_id],
            "boxes": [0, 0, 0, 0]
        }]

    # Save to JSON
    with open("instance_pin_boundary_map.json", "w") as f:
        json.dump(node_map, f, indent=1)
    print("✅ Saved instance-to-pin-boundary mapping to instance_pin_boundary_map.json")

    # --- Add-on: Build cluster_boxes_map.json for all levels using instance_pin_boundary_map.json ---
    with open("level_cluster_map_unsorted.json") as f:
        level_cluster_map = json.load(f)
    with open("instance_pin_boundary_map.json") as f:
        pin_boundary_map = json.load(f)

    def get_boxes(node_id):
        """Return the boxes for a node from the pin boundary map, or None if not found or all zeros."""
        entry = pin_boundary_map.get(str(node_id), [])
        for pin in entry:
            boxes = pin.get("boxes", [0,0,0,0])
            if any(boxes):
                return boxes
        return None

    def get_leaf_nodes(node, level, level_cluster_map):
        if level == 0:
            return [int(node)] if isinstance(node, (int, str)) and str(node).isdigit() else []
        node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
        for cluster_id, node_list in level_cluster_map[level-1].items():
            node_list_int = [int(n.split("N")[-1]) if isinstance(n, str) else n for n in node_list]
            if node_id in node_list_int:
                leafs = []
                for child in node_list:
                    leafs.extend(get_leaf_nodes(child, level-1, level_cluster_map))
                return leafs
        return []

    cluster_boxes = {}

    # Level 0
    level0 = level_cluster_map[0]
    cluster_boxes["level_0"] = {}
    for cluster_id, node_list in level0.items():
        cluster_boxes["level_0"][str(cluster_id)] = {}
        for node_id in node_list:
            boxes = get_boxes(node_id)
            cluster_boxes["level_0"][str(cluster_id)][str(node_id)] = {
                "boxes": [int(round(x * 18)) for x in boxes] if boxes is not None else [0,0,0,0]
            }

    # Higher levels
    for level in range(1, len(level_cluster_map)):
        level_key = f"level_{level}"
        cluster_boxes[level_key] = {}
        level_map = level_cluster_map[level]
        for cluster_id, node_list in level_map.items():
            cluster_boxes[level_key][str(cluster_id)] = {}
            for supernode in node_list:
                leaf_nodes = get_leaf_nodes(supernode, level, level_cluster_map)
                boxes_list = []
                for leaf in leaf_nodes:
                    boxes = get_boxes(leaf)
                    if boxes is not None and any(boxes):
                        boxes_list.append(boxes)
                if boxes_list:
                    avg_boxes = np.mean(np.array(boxes_list), axis=0).tolist()
                    scaled_boxes = [int(round(x * 18)) for x in avg_boxes]
                else:
                    scaled_boxes = [0,0,0,0]
                cluster_boxes[level_key][str(cluster_id)][str(supernode)] = {
                    "boxes": scaled_boxes
                }

    with open("cluster_boxes_map.json", "w") as f:
        json.dump(cluster_boxes, f, indent=2)
    print("✅ Saved cluster_boxes_map.json")

if __name__ == "__main__":
    main("gcd_ihp-sg13g2.txt")