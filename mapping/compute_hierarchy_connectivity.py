import json
from collections import defaultdict
from extractor import DesignParser

# ----------------------------
# Load required data
# ----------------------------
with open("level_cluster_map_unsorted.json", "r") as f:
    level_cluster_map = json.load(f)

with open("cluster_area.json", "r") as f:
    raw_area = json.load(f)
    cluster_area = {int(k): {int(kk): vv for kk, vv in v.items()} for k, v in raw_area.items()}

design = DesignParser("ibex_nangate45.txt")

# ----------------------------
# Build node-level connectivity map
# ----------------------------
def build_node_connectivity_map(hypergraph):
    connectivity_map = defaultdict(set)
    for driver, sinks in hypergraph.items():
        all_nodes = [driver] + sinks
        for node in all_nodes:
            others = [n for n in all_nodes if n != node]
            connectivity_map[node].update(others)
    return {k: sorted(v) for k, v in connectivity_map.items()}

connectivity_map = build_node_connectivity_map(design.hypergraph)


# ----------------------------
# Build enriched connectivity per level
# ----------------------------
level_connectivity = {}

for level, level_cluster in enumerate(level_cluster_map):
    level_connectivity[level] = {}
    for cluster_id, node_list in level_cluster.items():
        enriched_nodes = []
        node_set = set()

        for node in node_list:
            try:
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = cluster_area[level].get(node_id, None)
                connections = connectivity_map.get(node_id, [])
                node_set.add(node_id)

                # Level 0: Keep full connectivity
                if level == 0:
                    enriched_nodes.append({
                        "node": node_id,
                        "area": area,
                        # "connections": connections,
                        "connection_count": len(connections)
                    })

            except Exception as e:
                print(f"[Error] Level {level} - Cluster {cluster_id} - Node {node}: {e}")

        # Level > 0: Compute cluster-level connections
        if level > 0:
            cluster_connections = set()
            for node in node_list:
                node_id = int(node.split("N")[-1])
                connected_nodes = connectivity_map.get(node_id, [])
                for other_id in connected_nodes:
                    for other_cluster, others in level_cluster.items():
                        if other_cluster == cluster_id:
                            continue
                        if any(int(x.split("N")[-1]) == other_id if isinstance(x, str) else x == other_id for x in others):
                            cluster_connections.add(other_cluster)
            enriched_nodes.append({
                "node": cluster_id,
                "area": cluster_area[level].get(int(cluster_id), None),
                # "connections": sorted(cluster_connections),
                "connection_count": len(cluster_connections)

            })

        level_connectivity[level][str(cluster_id)] = enriched_nodes

# ----------------------------
# Save output
# ----------------------------
with open("hierarchy_connectivity.json", "w") as f:
    json.dump(level_connectivity, f, indent=2)

print("✅ Saved connectivity to hierarchy_connectivity.json")


