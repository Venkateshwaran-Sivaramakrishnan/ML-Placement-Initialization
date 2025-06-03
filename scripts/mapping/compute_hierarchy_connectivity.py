import argparse
import json
from collections import defaultdict
from extractor import DesignParser
import numpy as np

def compute_hierarchy_connectivity(design = "gcd", tech = "ihp-sg13g2"):
    # ----------------------------
    # Load required data
    # ----------------------------
    with open("level_cluster_map_unsorted.json", "r") as f:
        level_cluster_map = json.load(f)

    with open("cluster_area.json", "r") as f:
        raw_area = json.load(f)
        cluster_area = {int(k): {int(kk): vv for kk, vv in v.items()} for k, v in raw_area.items()}

    with open("cluster_netlists.json", "r") as f:
        cluster_netlists = json.load(f)

    with open("cluster_boxes_map.json", "r") as f:
        cluster_boxes_map = json.load(f)

    num_levels = len(level_cluster_map)
    filepath = f"{design}_{tech}.txt"
    design_parser = DesignParser(filepath)

    # ----------------------------
    # Build enriched connectivity per level
    # ----------------------------
    level_connectivity = {}

    for level, level_cluster in enumerate(level_cluster_map):
        level_key = f"level_{level}"
        level_connectivity[level] = {}
        for cluster_id, node_list in level_cluster.items():
            node_info = []

            # --- Gather area for normalization ---
            area_list = []
            for node in node_list:
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = cluster_area[level].get(node_id, 0)
                area_list.append(area)
            max_area = max(area_list) if area_list else 1

            # --- Get netlists for this cluster ---
            netlists = cluster_netlists[level_key][str(cluster_id)]
            # node_list may contain ints or strings, so convert to str for lookup
            node_ids_str = [str(int(node.split("N")[-1]) if isinstance(node, str) else node) for node in node_list]

            # --- Build internal_connections dicts ---
            internal_connections_dicts = []
            for i, node_id in enumerate(node_ids_str):
                nets_i = set(netlists.get(node_id, []))
                internal_connections = {}
                for j, other_id in enumerate(node_ids_str):
                    if i == j:
                        continue
                    nets_j = set(netlists.get(other_id, []))
                    shared_nets = nets_i & nets_j
                    if shared_nets:
                        internal_connections[int(other_id)] = len(shared_nets)
                internal_connections_dicts.append(internal_connections)

            # Compute total_internal_cons for each node
            total_internal_cons_list = [sum(d.values()) for d in internal_connections_dicts]
            max_total_internal_cons = max(total_internal_cons_list) if total_internal_cons_list else 1

            # --- Compose node_info ---
            for idx, node in enumerate(node_list):
                node_id = int(node.split("N")[-1]) if isinstance(node, str) else node
                area = area_list[idx]
                area_score = area / max_area if max_area else 0
                S = 29 if area_score >= 1.0 else int(area_score * 30)
                total_internal_cons = total_internal_cons_list[idx]
                internal_conn_score = total_internal_cons / max_total_internal_cons if max_total_internal_cons else 0
                ca_score = (area_score + internal_conn_score) / 2

                # --- Get R (boxes) ---
                level_key = f"level_{level}"
                cluster_boxes = cluster_boxes_map[level_key][str(cluster_id)]
                # node_id as string for lookup (handles both int and str node names)
                node_key = str(node) if str(node) in cluster_boxes else str(int(node.split("N")[-1]) if isinstance(node, str) else node)
                R = cluster_boxes.get(node_key, {}).get("boxes", [0, 0, 0, 0])

                node_info.append({
                    "node": node_id,
                    "area": area,
                    "internal_connections": internal_connections_dicts[idx],  # {node_id: num_shared_nets}
                    "total_internal_cons": total_internal_cons,
                    "area_score": area_score,
                    "S": S,
                    "internal_conn_score": internal_conn_score,
                    "ca_score": ca_score,
                    "R": R
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
                connected = set(this_node.get("internal_connections", {}).keys())
                for j, n2 in enumerate(node_ids):
                    row.append(1 if n2 in connected else 0)
                A.append(row)
            for i, node in enumerate(node_info):
                node["A"] = A[i]  # Each node's A is now length n, not padded/truncated

            # --- Cluster-level T, S, A, R as tensors with start/end token and padding ---
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

            cluster_R_raw = [node["R"] for node in node_info]
            R_padded = [[19, 19, 19, 19]] + cluster_R_raw[:8]
            R_padded.append([18, 18, 18, 18])
            while len(R_padded) < 10:
                R_padded.append([0, 0, 0, 0])
            cluster_R = np.array(R_padded)

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
            cluster_R = cluster_R.tolist()

            # --- Compose final cluster representation ---
            level_connectivity[level][str(cluster_id)] = {
                "node_info": node_info,
                "cluster_info": {
                    "T": cluster_T,
                    "S": cluster_S,
                    "A": cluster_A,
                    "R": cluster_R
                }
            }

    # ----------------------------
    # Save output
    # ----------------------------
    with open("hierarchy_connectivity.json", "w") as f:
        json.dump(level_connectivity, f, indent=2)

    print("✅ Saved connectivity to hierarchy_connectivity.json")

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
            R = np.array(cluster_data["cluster_info"]["R"])
            # Append as a tuple or dict
            cluster_tensor_data.append({
                "level": int(level),
                "cluster_id": int(cluster_id),
                "node_list": node_list,
                "T": T,
                "A": A,
                "S": S,
                "R": R
            })

    # Save as npy (list of dicts)
    np.save("cluster_tensor_data.npy", cluster_tensor_data, allow_pickle=True)
    print("✅ Saved cluster tensor data to cluster_tensor_data.npy")


def parse_args():
    parser = argparse.ArgumentParser(description="Compute area for hierarchy clusters")
    parser.add_argument("--design", type=str, required=True, help="Design name (e.g., ibex_nangate45)")
    parser.add_argument("--tech", type=str, required=True, help="Technology name (e.g., nangate45)")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    design = args.design
    tech = args.tech
    compute_hierarchy_connectivity(design, tech)