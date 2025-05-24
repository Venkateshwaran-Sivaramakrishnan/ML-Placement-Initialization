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

'''

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

'''

for level, level_cluster in enumerate(level_cluster_map):
    level_connectivity[level] = {}
    for cluster_id, node_list in level_cluster.items():
        enriched_nodes = []

        # Gather area and internal connectivity for normalization
        area_list = []
        internal_conn_list = []
        for node in node_list:
            try:
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = cluster_area[level].get(node_id, None)
                connections = connectivity_map.get(node_id, [])
                internal_conns = [
                    other for other in node_list
                    if (int(other.split("N")[-1]) if isinstance(other, str) else other) in connections
                    and other != node
                ]
                internal_conns = sorted(
                    [int(x.split("N")[-1]) if isinstance(x, str) else x for x in internal_conns]
                )
                area_list.append(area if area is not None else 0)
                internal_conn_list.append(len(internal_conns))
            except Exception as e:
                print(f"[Error] Level {level} - Cluster {cluster_id} - Node {node}: {e}")
                area_list.append(0)
                internal_conn_list.append(0)

        max_area = max(area_list) if area_list else 1
        max_internal_conn = max(internal_conn_list) if internal_conn_list else 1

        for idx, node in enumerate(node_list):
            try:
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = area_list[idx]
                connections = connectivity_map.get(node_id, [])
                internal_conns = [
                    other for other in node_list
                    if (int(other.split("N")[-1]) if isinstance(other, str) else other) in connections
                    and other != node
                ]
                internal_conns = sorted(
                    [int(x.split("N")[-1]) if isinstance(x, str) else x for x in internal_conns]
                )
                internal_conn = len(internal_conns)

                # Normalized scores
                area_score = area / max_area if max_area else 0
                # Bin area_score into 30 bins (1 to 29)
                if area_score >= 1.0:
                    S = 29
                else:
                    S = int(area_score * 30)
                internal_conn_score = internal_conn / max_internal_conn if max_internal_conn else 0
                ca_score = (area_score + internal_conn_score) / 2

                if level == 0:
                    enriched_nodes.append({
                        "node": node_id,
                        "area": area,
                        "connection_count": len(connections),
                        "internal_connections": internal_conns,
                        "area_score": area_score,
                        "S": S,
                        "internal_conn_score": internal_conn_score,
                        "ca_score": ca_score
                    })

            except Exception as e:
                print(f"[Error] Level {level} - Cluster {cluster_id} - Node {node}: {e}")

        # For level > 0 (cluster-level)
        if level > 0:
            cluster_connections = set()
            internal_conns = set()
            for node in node_list:
                node_id = int(node.split("N")[-1])
                connected_nodes = connectivity_map.get(node_id, [])
                for other_cluster, others in level_cluster.items():
                    if other_cluster == cluster_id:
                        for other in others:
                            other_id = int(other.split("N")[-1])
                            if other_id in connected_nodes and other_id != node_id:
                                internal_conns.add(other_cluster)
                    else:
                        if any(
                            int(x.split("N")[-1]) == other_id if isinstance(x, str) else x == other_id
                            for x in others for other_id in connected_nodes
                        ):
                            cluster_connections.add(other_cluster)

            area = cluster_area[level].get(int(cluster_id), None)
            internal_conn = len(internal_conns)
            area_score = area / max_area if max_area else 0
            if area_score >= 1.0:
                S = 29
            else:
                S = int(area_score * 30)
            internal_conn_score = internal_conn / max_internal_conn if max_internal_conn else 0
            ca_score = (area_score + internal_conn_score) / 2

            enriched_nodes.append({
                "node": cluster_id,
                "area": area,
                "connection_count": len(cluster_connections),
                "internal_connections": sorted(internal_conns),
                "area_score": area_score,
                "S": S,
                "internal_conn_score": internal_conn_score,
                "ca_score": ca_score
            })

        # Sort by ca_score descending
        enriched_nodes = sorted(enriched_nodes, key=lambda x: x["ca_score"], reverse=True)

        # Assign rank (1 = highest ca_score) and T value
        T_Dict = [1, 6, 4, 5, 7, 2, 3]
        for idx, node in enumerate(enriched_nodes):
            node["rank"] = idx + 1
            # Assign T based on rank, if rank exceeds T_Dict length, use last value
            node["T"] = T_Dict[idx] if idx < len(T_Dict) else T_Dict[-1]

        # --- Add one-hot connectivity encoding 'A' ---
        # Build node id list in current order
        node_ids = [n["node"] for n in enriched_nodes]
        node_id_to_index = {nid: i for i, nid in enumerate(node_ids)}
        n = len(node_ids)
        # Build adjacency matrix A: A[i][j] = 1 if node i connects to node j, else 0
        A = []
        for i, n1 in enumerate(node_ids):
            row = []
            # For level 0, use connectivity_map; for higher, use internal_connections
            if level == 0:
                connected = set(connectivity_map.get(n1, []))
                for j, n2 in enumerate(node_ids):
                    row.append(1 if n2 in connected else 0)
            else:
                # For clusters, use internal_connections field if available
                this_node = enriched_nodes[i]
                connected = set(this_node.get("internal_connections", []))
                for j, n2 in enumerate(node_ids):
                    row.append(1 if n2 in connected else 0)
            A.append(row)
        # Attach A to each node as its row
        for i, node in enumerate(enriched_nodes):
            node["A"] = A[i]

        level_connectivity[level][str(cluster_id)] = enriched_nodes



# ----------------------------
# Save output
# ----------------------------
with open("hierarchy_connectivity.json", "w") as f:
    json.dump(level_connectivity, f, indent=2)

print("✅ Saved connectivity to hierarchy_connectivity.json")


