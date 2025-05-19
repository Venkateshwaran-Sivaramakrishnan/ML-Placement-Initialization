import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import math
import json
import networkx as nx


def load_pickle(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)


def build_incidence_matrix(io_pins, instances, hypergraph):
    filtered_instances = {
        vid: inst for vid, inst in instances.items()
        if not inst["is_macro"] and not inst["is_fixed"]
    }
    all_vertices = list(filtered_instances.keys())
    all_nets = list(hypergraph.keys())
    v_idx = {vid: i for i, vid in enumerate(all_vertices)}
    n_idx = {nid: j for j, nid in enumerate(all_nets)}

    rows, cols = [], []
    for net_id, vertices in hypergraph.items():
        for v in vertices:
            if v in v_idx:
                rows.append(v_idx[v])
                cols.append(n_idx[net_id])

    data = np.ones(len(rows))
    H = csr_matrix((data, (rows, cols)), shape=(len(v_idx), len(n_idx)))
    return H, all_vertices


def compute_embedding(H, dim):
    A = H @ H.T
    A.data[np.isinf(A.data)] = 0
    A.data[np.isnan(A.data)] = 0
    if A.nnz == 0 or A.shape[0] < dim or A.shape[1] <= 1:
        return np.zeros((A.shape[0], dim))
    try:
        svd = TruncatedSVD(n_components=min(dim, A.shape[1] - 1), algorithm='randomized', random_state=42)
        return svd.fit_transform(A)
    except Exception:
        return np.zeros((A.shape[0], dim))


def cluster(U, max_cluster_size, expected_num_clusters=None):
    num_nodes = U.shape[0]
    if expected_num_clusters is None:
        expected_num_clusters = math.ceil(num_nodes / max_cluster_size)
    unique_rows = np.unique(U, axis=0)
    max_kmeans_clusters = min(expected_num_clusters, len(unique_rows), num_nodes)
    kmeans = KMeans(n_clusters=max_kmeans_clusters, n_init=10, random_state=42)
    initial_labels = kmeans.fit_predict(U)

    final_labels = -np.ones_like(initial_labels)
    current_label = 0
    for cluster_id in np.unique(initial_labels):
        indices = np.where(initial_labels == cluster_id)[0]
        if len(indices) <= max_cluster_size:
            final_labels[indices] = current_label
            current_label += 1
        else:
            for i in range(0, len(indices), max_cluster_size):
                sub_indices = indices[i:i + max_cluster_size]
                final_labels[sub_indices] = current_label
                current_label += 1
    if np.any(final_labels == -1):
        raise ValueError("Some nodes were not assigned a cluster.")
    return final_labels


def hierarchical_spectral_clustering(H, N, cluster_stop_length, instance_ids):
    hierarchy = []
    current_H = H
    level = 0
    current_nodes = instance_ids
    while True:
        U = compute_embedding(current_H, dim=2)
        num_nodes = U.shape[0]
        if num_nodes <= max(N, cluster_stop_length):
            break
        num_clusters = math.ceil(num_nodes / N)
        labels = cluster(U, max_cluster_size=N, expected_num_clusters=num_clusters)
        print(f"Level {level} → {num_nodes} nodes → {len(np.unique(labels))} clusters")
        parent_map = {current_nodes[i]: int(labels[i]) for i in range(len(labels))}
        hierarchy.append((labels, U, current_nodes, parent_map))
        level += 1
        _, labels = np.unique(labels, return_inverse=True)
        num_supernodes = len(np.unique(labels))
        rows = labels
        cols = np.arange(len(labels))
        data = np.ones(len(labels))
        current_H = csr_matrix((data, (rows, cols)), shape=(num_supernodes, len(labels)))
        current_nodes = [f"L{level}_N{i}" for i in range(num_supernodes)]
    return hierarchy


def export_hierarchy(hierarchy, out_file="hierarchy.json"):
    hierarchy_data = []
    for level, (labels, _, node_ids, _) in enumerate(hierarchy):
        if len(labels) != len(node_ids):
            raise ValueError(f"Mismatch at level {level}: {len(labels)} labels vs {len(node_ids)} nodes")
        level_data = [{"node": node_ids[i], "cluster": int(labels[i])} for i in range(len(labels))]
        hierarchy_data.append({"level": level, "clusters": level_data})
    with open(out_file, "w") as f:
        json.dump(hierarchy_data, f, indent=2)
    print(f"Exported hierarchy structure to {out_file}")


def plot_hierarchy_tree(hierarchy, out_file="hierarchy_tree.svg"):
    G = nx.DiGraph()
    pos = {}
    y_gap = 10
    x_gap = 1.5
    node_mapping = {}
    level_positions = {}
    parent_to_children = {}

    for level in range(1, len(hierarchy)):
        _, _, node_ids, parent_map = hierarchy[level]
        for nid in node_ids:
            parent_cid = parent_map[nid]
            parent_name = f"L{level-1}_C{parent_cid}"
            child_cid = hierarchy[level][0][node_ids.index(nid)]
            child_name = f"L{level}_C{child_cid}"
            parent_to_children.setdefault(parent_name, set()).add(child_name)

    x_cursor = 0
    for level, (labels, _, node_ids, _) in enumerate(hierarchy):
        cluster_to_nodes = {}
        for i, cid in enumerate(labels):
            cluster_to_nodes.setdefault(cid, []).append(node_ids[i])
        level_clusters = sorted(cluster_to_nodes.keys())
        level_positions[level] = {}
        for cid in level_clusters:
            cluster_name = f"L{level}_C{cid}"
            if cluster_name in pos:
                continue
            G.add_node(cluster_name)
            pos[cluster_name] = (x_cursor, -level * y_gap)
            level_positions[level][cid] = x_cursor
            x_cursor += x_gap

    for parent, children in parent_to_children.items():
        if all(child in pos for child in children):
            xs = [pos[child][0] for child in children]
            cx = sum(xs) / len(xs)
            cy = pos[parent][1] if parent in pos else -y_gap * int(parent[1])
            pos[parent] = (cx, cy)

    for level in range(1, len(hierarchy)):
        _, _, node_ids, parent_map = hierarchy[level]
        for i, nid in enumerate(node_ids):
            child_cid = hierarchy[level][0][i]
            child_name = f"L{level}_C{child_cid}"
            parent_cid = parent_map[nid]
            parent_name = f"L{level-1}_C{parent_cid}"
            G.add_edge(parent_name, child_name)

    plt.figure(figsize=(max(12, x_cursor * 0.6), len(hierarchy) * 2.5))
    nx.draw(G, pos, with_labels=True, node_size=800, font_size=8, arrows=True)
    plt.title("Clean Hierarchy Tree of Clustering")
    plt.tight_layout()
    plt.savefig(out_file)
    print(f"Saved hierarchy tree to {out_file}")


def main(filepath, N=5, cluster_stop_length=10):
    data = load_pickle(filepath)
    H, instance_ids = build_incidence_matrix(data["io_pins"], data["instances"], data["hypergraph"])
    hierarchy = hierarchical_spectral_clustering(H, N, cluster_stop_length, instance_ids)

    labels, _, _, _ = hierarchy[0]
    instance_labels = {instance_ids[i]: int(labels[i]) for i in range(len(labels))}
    with open("instance_cluster_map.json", "w") as f:
        json.dump(instance_labels, f, indent=2)
    print("Exported instance-to-cluster mapping to instance_cluster_map.json")

    export_hierarchy(hierarchy)

    plt.figure(figsize=(10, 6))
    scatter_x = np.arange(len(labels))
    scatter_y = labels
    plt.scatter(scatter_x, scatter_y, c=labels, cmap='tab20', s=10)
    plt.title("Level 0: Instance-to-Cluster Mapping")
    plt.xlabel("Instance Index")
    plt.ylabel("Cluster ID")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig("instance_cluster_plot.svg")
    print("Saved cluster visualization to instance_cluster_plot.svg")

    plot_hierarchy_tree(hierarchy, out_file="hierarchy_tree.svg")


if __name__ == "__main__":
    main("ibex_core.pkl", N=5, cluster_stop_length=10)