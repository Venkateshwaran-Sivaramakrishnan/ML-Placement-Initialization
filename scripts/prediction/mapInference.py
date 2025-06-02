import pickle
import json
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Placement propagation script")
parser.add_argument("-d", "--design", required=True, help="Design name (e.g., gcd)")
args = parser.parse_args()

# Use the parsed arguments
design = args.design

# Load gcd.pkl
with open("gcd.pkl", "rb") as f:
    data = pickle.load(f)

# Load the npy file (list of dictionaries)
cluster_tensor_data_predict = np.load("cluster_tensor_data_predict.npy", allow_pickle=True)

# Convert to a Python list (optional but recommended for iteration)
cluster_tensor_data_predict = cluster_tensor_data_predict.tolist()

core = data["design_info"]["core_region"]
core_xmin, core_ymin = core["lx"], core["ly"]
core_xmax, core_ymax = core["ux"], core["uy"]
core_width = core_xmax - core_xmin
core_height = core_ymax - core_ymin
core_area = core_width * core_height

print(f"Core Region:")
print(f"  lx: {core_xmin}")
print(f"  ly: {core_ymin}")
print(f"  ux: {core_xmax}")
print(f"  uy: {core_ymax}")
print(f"  Core Width: {core_width}")
print(f"  Core Height: {core_height}")
print(f"  Core Area: {core_area}")

# Load cluster_area.json
with open("cluster_area.json", "r") as f:
    cluster_area = json.load(f)

# Extract max level (last key) and its "0" entry
max_level_area = str(max(map(int, cluster_area.keys())))
cell_area = cluster_area[max_level_area]["0"]

# Compute core area and remaining area
core_area = core_width * core_height
remaining_area = core_area - cell_area
target_area = cell_area + 0.5 * remaining_area

# Compute square side length
square_side = int(math.sqrt(target_area))

# Center the square within the core
core_xmin, core_ymin = core["lx"], core["ly"]
core_xmax, core_ymax = core["ux"], core["uy"]
core_center_x = (core_xmin + core_xmax) // 2
core_center_y = (core_ymin + core_ymax) // 2

square_xmin = core_center_x - square_side // 2
square_xmax = core_center_x + square_side // 2
square_ymin = core_center_y - square_side // 2
square_ymax = core_center_y + square_side // 2

if (remaining_area <= 0):
    square_xmin = core_xmin
    square_xmax = core_xmax
    square_ymin = core_ymin
    square_ymax = core_ymax

# Output result
print("\nTarget Area:", target_area)
print("Square bounds:")
print(f"  X: {square_xmin} → {square_xmax}")
print(f"  Y: {square_ymin} → {square_ymax}")

# Organize nodes by level
level_dict = {}
for entry in cluster_tensor_data_predict:
    level = entry["level"]
    level_dict.setdefault(level, []).append(entry)

# Start from highest level
node_position_map = {}
max_level = max(entry["level"] for entry in cluster_tensor_data_predict)
print(max_level)
for level in sorted(level_dict.keys(), reverse=True):
    for node in level_dict[level]:
        if level == max_level:
            # Assign bounding box for root nodes
            node["position"] = [square_xmin, square_ymin, square_xmax, square_ymax]
            for idx in range(len(node["node_list"])):
                # Scale each child's 128x128 grid to this node's bounding box
                scale_x = square_xmax - square_xmin
                scale_y = square_ymax - square_ymin
                x = node["coordinates"][idx][0][0]
                y = node["coordinates"][idx][0][1]
                w = node["coordinates"][idx][1][0]
                h = node["coordinates"][idx][1][1]
                child_xmin = square_xmin + (x / 128) * scale_x
                child_ymin = square_ymin + (y / 128) * scale_y
                child_xmax = square_xmin + (w / 128) * scale_x
                child_ymax = square_ymin + (h / 128) * scale_y

                child_level = level - 1
                item = node["node_list"][idx]
                for child_node in cluster_tensor_data_predict:
                    if child_node["level"] == child_level and child_node["cluster_id"] == item:
                        child_node["position"] = [child_xmin, child_ymin, child_xmax, child_ymax]
                        break

        elif level >= 1:
            parent_pos = node.get("position")
            if parent_pos is None:
                continue
            pxmin, pymin, pxmax, pymax = parent_pos
            for idx in range(len(node["node_list"])):
                scale_x = pxmax - pxmin
                scale_y = pymax - pymin
                x = node["coordinates"][idx][0][0]
                y = node["coordinates"][idx][0][1]
                w = node["coordinates"][idx][1][0]
                h = node["coordinates"][idx][1][1]
                child_xmin = pxmin + (x / 128) * scale_x
                child_ymin = pymin + (y / 128) * scale_y
                child_xmax = pxmin + (w / 128) * scale_x
                child_ymax = pymin + (h / 128) * scale_y

                child_level = level - 1
                item = node["node_list"][idx]
                for child_node in cluster_tensor_data_predict:
                    if child_node["level"] == child_level and child_node["cluster_id"] == item:
                        child_node["position"] = [child_xmin, child_ymin, child_xmax, child_ymax]
                        break

        elif level == 0:
            parent_pos = node.get("position")
            if parent_pos is None:
                continue
            pxmin, pymin, pxmax, pymax = parent_pos
            for idx in range(len(node["node_list"])):
                scale_x = pxmax - pxmin
                scale_y = pymax - pymin
                x = node["coordinates"][idx][0][0]
                y = node["coordinates"][idx][0][1]
                w = node["coordinates"][idx][1][0]
                h = node["coordinates"][idx][1][1]
                child_xmin = pxmin + (x / 128) * scale_x
                child_ymin = pymin + (y / 128) * scale_y

                node_position_map[node["node_list"][idx]] = [child_xmin, child_ymin]

#for entry in cluster_tensor_data_predict:
#    if entry["level"] == 0:
#        print(entry)

# Extract all x and y coordinates
xs = []
ys = []

for node_id, (x, y) in node_position_map.items():
    xs.append(x)
    ys.append(y)

# Plot all coordinates
plt.figure(figsize=(8, 8))
plt.scatter(xs, ys, s=10, color='blue', label='Nodes')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Node Positions from node_position_map")
plt.grid(True)
plt.legend()
plt.axis("equal")
plt.tight_layout()

# Save the image
plt.savefig("node_positions.png", dpi=300)

# Optionally display
# plt.show()

with open(f"{design}.json", "r") as f:
    design_json = json.load(f)

# Create a flat mapping: node_id → position

print(node_position_map)

with open("init_placement_test.txt", "w") as f:
    for node_id, (x, y) in node_position_map.items():
        str_id = str(node_id)
        instance = design_json["instances"].get(str_id)
        if instance:
            instance_name = instance.get("instance_name", "UNKNOWN")
            f.write(f"{instance_name} {x} {y}\n")
