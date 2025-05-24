import json
from collections import defaultdict
from mapping import get_node_geometry
from extractor import DesignParser

# Load the hierarchy JSON
with open("hierarchy.json", "r") as f:
    hierarchy = json.load(f)

# Initialize design parser
design = DesignParser("ibex_nangate45.txt")

# Step 1: Build level-wise cluster-to-nodes map
level_cluster_map = []
for level_info in hierarchy:
    # print(f"Level {level_info['level']}:")
    cluster_to_nodes = defaultdict(list)
    for entry in level_info["clusters"]:
        cluster_to_nodes[entry["cluster"]].append(entry["node"])    
    # print("cluster_to_nodes:", cluster_to_nodes)
    level_cluster_map.append(cluster_to_nodes)

# Step 2: Compute area at level 0 and level 1
cluster_area = {}
cluster_area[0] = {}
cluster_area[1] = {}
level_0_clusters = level_cluster_map[0]
for cluster_id, node_list in level_0_clusters.items():
    total_area = 0
    for node_id in node_list:
        geom = get_node_geometry(design,node_id)
        area = geom["width"] * geom["height"]
        cluster_area[0][node_id] = area
        total_area += area
    cluster_area[1][cluster_id] = total_area

# Step 3: Compute area at higher levels recursively
for level in range(1, len(level_cluster_map)):
    next_level_clusters = level_cluster_map[level]
    new_cluster_area = {}
    for cluster_id, child_nodes in next_level_clusters.items():
        total_area = 0
        for child in child_nodes:
            child_id = int(child.split("N")[-1])
            if child_id not in cluster_area[level].keys():
                print(f"child_id: {child_id}")
                print(f"cluster_area[{level}].keys(): {cluster_area[level].keys()}")
                raise ValueError(f"Cluster {child_id} has no known area at level {level}")
            total_area += cluster_area[level][child_id]
        new_cluster_area[cluster_id] = total_area
    cluster_area[level+1] = new_cluster_area

with open("cluster_area.json", "w") as f:
    json.dump(cluster_area, f, indent=2)

with open("level_cluster_map_unsorted.json", "w") as f:
    json.dump(level_cluster_map, f, indent=2)

# Step 5: Arrange the nodes/subclusters in the same order as the cluster area
sorted_cluster_children = {}  # Final result

for level, level_cluster in enumerate(level_cluster_map):
    sorted_cluster_children[level] = {}
    for cluster_id, node_list in level_cluster.items():
        children_with_areas = []
        for node in node_list:
            try:
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = cluster_area[level][node_id]
                children_with_areas.append({"node": node_id, "area": area})
            except KeyError as e:
                raise KeyError(f"[Level {level}] Area not found for node {node_id} in cluster_area[{level}]") from e
            except IndexError as e:
                raise IndexError(f"[Level {level}] Index error while accessing cluster_area.") from e

            # Sort by area descending
            children_with_areas.sort(key=lambda x: x["area"], reverse=True)

            # Add area_index after sorting
            for idx, item in enumerate(children_with_areas):
                item["area_index"] = idx

            sorted_cluster_children[level][cluster_id] = children_with_areas


with open("level_cluster_map_sorted.json", "w") as f:
    json.dump(sorted_cluster_children, f, indent=2)