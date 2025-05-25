import argparse
import json
from collections import defaultdict
from extractor import DesignParser
import numpy as np

# ----------------------------
# Load required data
# ----------------------------
with open("level_cluster_map_unsorted.json", "r") as f:
    level_cluster_map = json.load(f)

with open("cluster_area.json", "r") as f:
    raw_area = json.load(f)
    cluster_area = {int(k): {int(kk): vv for kk, vv in v.items()} for k, v in raw_area.items()}

# Initialize design parser
def parse_args():
    parser = argparse.ArgumentParser(description="Compute area for hierarchy clusters")
    parser.add_argument("--design", type=str, required=True, help="Design name (e.g., ibex_nangate45)")
    parser.add_argument("--tech", type=str, required=True, help="Technology name (e.g., nangate45)")
    args = parser.parse_args()
    return args

args = parse_args()

filepath = args.design + "_" + args.tech + ".txt"
design = DesignParser(filepath)
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
        node_info = []

        # For level 0, node_list contains node IDs
        # For level > 0, node_list contains cluster IDs from previous level

        # --- Gather area for normalization ---
        area_list = []
        for node in node_list:
            node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
            if level == 0:
                area = cluster_area[level].get(node_id, 0)
            else:
                area = cluster_area[level-1].get(node_id, 0)
            area_list.append(area)
        max_area = max(area_list) if area_list else 1

        # --- Build child-to-members map for level > 0 ---
        if level > 0:
            prev_level_map = level_cluster_map[level-1]
            child_to_members = {}
            for child in node_list:
                members = prev_level_map.get(str(child), []) if isinstance(prev_level_map, dict) else prev_level_map.get(child, [])
                child_to_members[child] = [int(m.split("N")[-1]) if isinstance(m, str) else m for m in members]

        # --- Compute internal connectivity for each node/cluster ---
        internal_conn_list = []
        for idx, node in enumerate(node_list):
            node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
            if level == 0:
                # Internal connections: how many other nodes in this cluster is this node connected to
                connections = connectivity_map.get(node_id, [])
                internal_conns = [
                    other for other in node_list
                    if (int(other.split("N")[-1]) if isinstance(other, str) else other) in connections
                    and other != node
                ]
                internal_conn_list.append(len(internal_conns))
            else:
                # For clusters: sum of connections between members of this child cluster and members of other child clusters in this cluster
                members = set(child_to_members[node])
                conn_count = 0
                for other_idx, other in enumerate(node_list):
                    if other == node:
                        continue
                    other_members = set(child_to_members[other])
                    for m in members:
                        conn_count += len(set(connectivity_map.get(m, [])) & other_members)
                internal_conn_list.append(conn_count)

        max_internal_conn = max(internal_conn_list) if internal_conn_list else 1

        # --- Compose node_info ---
        for idx, node in enumerate(node_list):
            node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
            area = area_list[idx]
            area_score = area / max_area if max_area else 0
            S = 29 if area_score >= 1.0 else int(area_score * 30)
            internal_conn = internal_conn_list[idx]
            internal_conn_score = internal_conn / max_internal_conn if max_internal_conn else 0
            ca_score = (area_score + internal_conn_score) / 2

            if level == 0:
                connections = connectivity_map.get(node_id, [])
                internal_conns = [
                    other for other in node_list
                    if (int(other.split("N")[-1]) if isinstance(other, str) else other) in connections
                    and other != node
                ]
                internal_conns = sorted(
                    [int(x.split("N")[-1]) if isinstance(x, str) else x for x in internal_conns]
                )
                node_info.append({
                    "node": node_id,
                    "area": area,
                    "connection_count": len(connections),
                    "internal_connections": internal_conns,
                    "area_score": area_score,
                    "S": S,
                    "internal_conn_score": internal_conn_score,
                    "ca_score": ca_score
                })
            else:
                # For clusters, we can optionally store which other clusters this cluster is connected to
                # (i.e., if any member of this cluster is connected to any member of another cluster)
                members = set(child_to_members[node])
                connected_clusters = []
                for other in node_list:
                    if other == node:
                        continue
                    other_members = set(child_to_members[other])
                    found = False
                    for m in members:
                        if set(connectivity_map.get(m, [])) & other_members:
                            found = True
                            break
                    if found:
                        connected_clusters.append(int(other.split("N")[-1]) if isinstance(other, str) else other)
                node_info.append({
                    "node": node_id,
                    "area": area,
                    "connection_count": len(connected_clusters),
                    "internal_connections": sorted(connected_clusters),
                    "area_score": area_score,
                    "S": S,
                    "internal_conn_score": internal_conn_score,
                    "ca_score": ca_score
                })

        # --- Sort node_info by ca_score descending ---
        node_info = sorted(node_info, key=lambda x: x["ca_score"], reverse=True)

        # --- Assign rank and T value ---
        T_Dict = [1, 6, 4, 5, 7, 2, 3]
        for idx, node in enumerate(node_info):
            node["rank"] = idx + 1
            node["T"] = T_Dict[idx] if idx < len(T_Dict) else T_Dict[-1]

        # --- Build adjacency matrix A ---
        node_ids = [n["node"] for n in node_info]
        n = len(node_ids)
        A = []
        for i, n1 in enumerate(node_ids):
            row = []
            this_node = node_info[i]
            connected = set(this_node.get("internal_connections", []))
            for j, n2 in enumerate(node_ids):
                row.append(1 if n2 in connected else 0)
            A.append(row)
        for i, node in enumerate(node_info):
            node["A"] = A[i]

        # --- Cluster-level T, S, A as tensors with start/end token and padding ---
        cluster_T_raw = [node["T"] for node in node_info]
        T_padded = [9] + cluster_T_raw[:8]
        T_padded.append(8)
        while len(T_padded) < 10:
            T_padded.append(0)
        cluster_T = np.array(T_padded)

        cluster_S_raw = [node["S"] for node in node_info]
        S_padded = [31] + cluster_S_raw[:8]
        S_padded.append(30)
        while len(S_padded) < 10:
            S_padded.append(0)
        cluster_S = np.array(S_padded)

        cluster_A_raw = [node["A"] for node in node_info]
        cluster_A_rows = []
        for a_row in cluster_A_raw[:8]:
            padded_row = list(a_row[:8]) + [0] * (8 - len(a_row))
            cluster_A_rows.append(padded_row)
        start_token = [1,1,1,1,1,1,1,1]
        end_token = [0,1,0,1,0,1,0,1]
        cluster_A = [start_token] + cluster_A_rows + [end_token]
        while len(cluster_A) < 10:
            cluster_A.append([0]*8)
        cluster_A = cluster_A[:10]
        cluster_A = np.array(cluster_A)

        # Convert tensors to lists for JSON serialization
        cluster_T = cluster_T.tolist()
        cluster_S = cluster_S.tolist()
        cluster_A = cluster_A.tolist()

        # --- Compose final cluster representation ---
        level_connectivity[level][str(cluster_id)] = {
            "node_info": node_info,
            "cluster_info": {
                "T": cluster_T,
                "S": cluster_S,
                "A": cluster_A
            }
        }


# ----------------------------
# Save output
# ----------------------------
with open("hierarchy_connectivity.json", "w") as f:
    json.dump(level_connectivity, f, indent=2)

print("Saved connectivity to hierarchy_connectivity.json")

# ----------------------------
# Save output as .npy for each cluster
# ----------------------------
cluster_tensor_data = []

for level, clusters in level_connectivity.items():
    for cluster_id, cluster_data in clusters.items():
        # Get node list in the cluster (in order)
        node_list = [node["node"] for node in cluster_data["node_info"]]
        # Get cluster-level T, S, A
        T = np.array(cluster_data["cluster_info"]["T"])
        S = np.array(cluster_data["cluster_info"]["S"])
        A = np.array(cluster_data["cluster_info"]["A"])
        # Append as a tuple or dict
        cluster_tensor_data.append({
            "level": int(level),
            "cluster_id": int(cluster_id),
            "node_list": node_list,
            "T": T,
            "A": A,
            "S": S
        })

# Save as npy (list of dicts)
np.save("cluster_tensor_data.npy", cluster_tensor_data, allow_pickle=True)

print("Saved cluster tensor data to cluster_tensor_data.npy")


