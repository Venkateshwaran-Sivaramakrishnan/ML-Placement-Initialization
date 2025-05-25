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

        # --- Node info ---
        node_info = []
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
                if area_score >= 1.0:
                    S = 29
                else:
                    S = int(area_score * 30)
                internal_conn_score = internal_conn / max_internal_conn if max_internal_conn else 0
                ca_score = (area_score + internal_conn_score) / 2

                if level == 0:
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

            except Exception as e:
                print(f"[Error] Level {level} - Cluster {cluster_id} - Node {node}: {e}")

        # For level > 0 (cluster-level)
        cluster_info = {}
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

            cluster_info = {
                "node": cluster_id,
                "area": area,
                "connection_count": len(cluster_connections),
                "internal_connections": sorted(internal_conns),
                "area_score": area_score,
                "S": S,
                "internal_conn_score": internal_conn_score,
                "ca_score": ca_score
            }

        # Sort node_info by ca_score descending
        node_info = sorted(node_info, key=lambda x: x["ca_score"], reverse=True)

        # Assign rank and T value
        T_Dict = [1, 6, 4, 5, 7, 2, 3]
        for idx, node in enumerate(node_info):
            node["rank"] = idx + 1
            node["T"] = T_Dict[idx] if idx < len(T_Dict) else T_Dict[-1]

        # Build node id list in current order
        node_ids = [n["node"] for n in node_info]
        n = len(node_ids)
        # Build adjacency matrix A: A[i][j] = 1 if node i connects to node j, else 0
        A = []
        for i, n1 in enumerate(node_ids):
            row = []
            if level == 0:
                connected = set(connectivity_map.get(n1, []))
                for j, n2 in enumerate(node_ids):
                    row.append(1 if n2 in connected else 0)
            else:
                this_node = node_info[i]
                connected = set(this_node.get("internal_connections", []))
                for j, n2 in enumerate(node_ids):
                    row.append(1 if n2 in connected else 0)
            A.append(row)
        for i, node in enumerate(node_info):
            node["A"] = A[i]

        # Cluster-level T, S, A as tensors with start/end token and padding for T and S and A
        cluster_T_raw = [node["T"] for node in node_info]
        # T: Start token = 9, End token = 8, pad with 0 to length 10
        T_padded = [9] + cluster_T_raw[:8]
        T_padded.append(8)
        while len(T_padded) < 10:
            T_padded.append(0)
        cluster_T = np.array(T_padded)

        cluster_S_raw = [node["S"] for node in node_info]
        # S: Start token = 31, End token = 30, pad with 0 to length 10
        S_padded = [31] + cluster_S_raw[:8]
        S_padded.append(30)
        while len(S_padded) < 10:
            S_padded.append(0)
        cluster_S = np.array(S_padded)

        # A: Start token = [1 1 1 1 1 1 1 1], End token = [0 1 0 1 0 1 0 1], pad with [0 0 0 0 0 0 0 0]
        cluster_A_raw = [node["A"] for node in node_info]
        # Pad each A row to length 8
        cluster_A_rows = []
        for a_row in cluster_A_raw[:8]:
            padded_row = list(a_row[:8]) + [0] * (8 - len(a_row))
            cluster_A_rows.append(padded_row)

        # Add start and end tokens
        start_token = [1,1,1,1,1,1,1,1]
        end_token = [0,1,0,1,0,1,0,1]
        cluster_A = [start_token] + cluster_A_rows + [end_token]
        # If less than 10 rows, pad with [0]*8 AFTER the end token
        while len(cluster_A) < 10:
            cluster_A.append([0]*8)
        # If more than 10 rows (shouldn't happen), truncate
        cluster_A = cluster_A[:10]
        cluster_A = np.array(cluster_A)

        # Convert tensors to lists for JSON serialization
        cluster_T = cluster_T.tolist()
        cluster_S = cluster_S.tolist()
        cluster_A = cluster_A.tolist()

        # Compose final cluster representation
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


