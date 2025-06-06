import argparse 
import pickle
import json
from collections import defaultdict
import networkx as nx
import numpy as np
from itertools import combinations
from sklearn.cluster import SpectralClustering
import pymetis


def parse_arguments():
    parser = argparse.ArgumentParser(description="Placement-driven hierarchical spectral clustering.")
    parser.add_argument("--design", required=True, help="Design name (e.g., gcd)")
    parser.add_argument("--N", type=int, default=5, help="Max number of nodes per cluster")
    parser.add_argument("--max_fanout", type=int, default=8, help="Ignore nets with more than this many nodes")
    return parser.parse_args()


def load_design(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)


def build_weighted_graph(instances, hypergraph, max_fanout):
    G = nx.Graph()
    for net, vertices in hypergraph.items():
        active_vertices = [v for v in vertices if v in instances]
        if len(active_vertices) > max_fanout:
            continue
        for i in range(len(active_vertices)):
            for j in range(i + 1, len(active_vertices)):
                u, v = active_vertices[i], active_vertices[j]
                if G.has_edge(u, v):
                    G[u][v]["weight"] += 1
                else:
                    G.add_edge(u, v, weight=1)
    return G


def hierarchical_spectral_clustering(G, N, level=0, base_cluster_id=0, prefix=""):
    results = []
    assigned_nodes = set()
    current_cluster_id = base_cluster_id
    print(f"Processing Cluster Level: {level}")

    if len(G) <= N:
        for node in G.nodes:
            results.append({"node": node, "cluster": current_cluster_id})
            assigned_nodes.add(node)
        return results, current_cluster_id + 1, assigned_nodes

    node_list = sorted(G.nodes())
    node_to_idx = {node: i for i, node in enumerate(node_list)}
    idx_to_node = {i: node for node, i in node_to_idx.items()}
    adjacency = [[] for _ in node_list]

    for u, v in G.edges():
        u_idx = node_to_idx[u]
        v_idx = node_to_idx[v]
        adjacency[u_idx].append(v_idx)
        adjacency[v_idx].append(u_idx)

    num_clusters = max(2, len(G) // N)
    try:
        _, parts = pymetis.part_graph(num_clusters, adjacency)
    except Exception as e:
        print(f"[WARN] METIS clustering failed at level {level} with {len(G)} nodes: {e}")
        for node in G.nodes:
            results.append({"node": node, "cluster": current_cluster_id})
            assigned_nodes.add(node)
        return results, current_cluster_id + 1, assigned_nodes

    label_to_nodes = defaultdict(list)
    for idx, label in enumerate(parts):
        label_to_nodes[label].append(idx_to_node[idx])

    for nodes in label_to_nodes.values():
        if len(nodes) <= N:
            for node in nodes:
                results.append({"node": node, "cluster": current_cluster_id})
                assigned_nodes.add(node)
            current_cluster_id += 1
        else:
            subgraph = G.subgraph(nodes)
            sub_results, current_cluster_id, sub_assigned = hierarchical_spectral_clustering(
                subgraph, N, level + 1, base_cluster_id=current_cluster_id, prefix=prefix)
            results.extend(sub_results)
            assigned_nodes.update(sub_assigned)

    return results, current_cluster_id, assigned_nodes


def build_supergraph(cluster_data, hypergraph, prefix="L"):
    cluster_to_nodes = defaultdict(set)
    for entry in cluster_data:
        cluster_to_nodes[entry["cluster"]].add(entry["node"])

    node_to_nets = defaultdict(set)
    for net, nodes in hypergraph.items():
        for node in nodes:
            node_to_nets[str(node)].add(net)

    SG = nx.Graph()
    cluster_ids = list(cluster_to_nodes.keys())
    for i in range(len(cluster_ids)):
        for j in range(i + 1, len(cluster_ids)):
            c1, c2 = cluster_ids[i], cluster_ids[j]
            shared_nets = 0
            for u in cluster_to_nodes[c1]:
                for v in cluster_to_nodes[c2]:
                    if node_to_nets[u] & node_to_nets[v]:
                        shared_nets += 1
            if shared_nets > 0:
                SG.add_edge(f"{prefix}_N{c1}", f"{prefix}_N{c2}", weight=shared_nets)
            else:
                SG.add_node(f"{prefix}_N{c1}")
                SG.add_node(f"{prefix}_N{c2}")
    return SG, cluster_to_nodes


def analyze_cluster_connectivity(cluster_data, hypergraph):
    cluster_data = [{"node": str(entry["node"]), "cluster": str(entry["cluster"])} for entry in cluster_data]
    node_to_nets = defaultdict(set)
    for net, nodes in hypergraph.items():
        for node in nodes:
            node_to_nets[str(node)].add(net)

    cluster_to_nodes = defaultdict(list)
    for entry in cluster_data:
        cluster_to_nodes[str(entry["cluster"])].append(str(entry["node"]))

    cluster_explanations = {}
    for cid, nodes in cluster_to_nodes.items():
        pairwise_info = []
        for u, v in combinations(nodes, 2):
            shared_nets = node_to_nets[str(u)].intersection(node_to_nets[str(v)])
            if shared_nets:
                pairwise_info.append({
                    "node_pair": [u, v],
                    "num_shared_nets": len(shared_nets),
                    "shared_nets": sorted(shared_nets)
                })
        cluster_explanations[cid] = {
            "num_nodes": len(nodes),
            "node_ids": sorted(nodes),
            "shared_pairs": pairwise_info
        }

    return cluster_explanations


def build_cluster_hierarchy(all_levels):
    hierarchy = {}
    base_level = all_levels[0]
    hierarchy[0] = defaultdict(set)
    for entry in base_level["clusters"]:
        hierarchy[0][entry["cluster"]].add(entry["node"])

    for level_info in all_levels[1:]:
        level = level_info["level"]
        hierarchy[level] = defaultdict(set)
        for entry in level_info["clusters"]:
            cluster_id = entry["cluster"]
            node_name = entry["node"]
            sublevel = int(node_name.split("_")[0][1:])
            subcluster = int(node_name.split("_N")[1])
            hierarchy[level][cluster_id].update(hierarchy[sublevel][subcluster])
    return hierarchy


def recursive_hierarchical_clustering(initial_cluster_data, hypergraph, N):
    all_levels = [{"level": 0, "clusters": initial_cluster_data}]
    hierarchy_mapping = {0: defaultdict(set)}
    for entry in initial_cluster_data:
        hierarchy_mapping[0][entry["cluster"]].add(entry["node"])

    current_data = initial_cluster_data
    prefix = "L1"
    level = 1

    while True:
        supergraph, cluster_to_nodes = build_supergraph(current_data, hypergraph, prefix)
        if len(supergraph) <= N:
            break

        clustered, _, _ = hierarchical_spectral_clustering(supergraph, N, level=level, prefix=prefix)
        renamed = [{"node": f"{prefix}_N{entry['node'].split('_N')[-1]}", "cluster": entry["cluster"]} for entry in clustered]
        all_levels.append({"level": level, "clusters": renamed})

        hierarchy_mapping[level] = defaultdict(set)
        for entry in clustered:
            cid = int(entry["node"].split("_N")[1])
            hierarchy_mapping[level][entry["cluster"]].update(cluster_to_nodes[cid])

        current_data = [
            {"node": node, "cluster": cid}
            for cid, nodes in hierarchy_mapping[level].items()
            for node in nodes
        ]
        level += 1
        prefix = f"L{level}"

    return all_levels, hierarchy_mapping


def main(filepath, args):
    data = load_design(filepath)

    filtered_instances = {
        vid: inst for vid, inst in data["instances"].items()
        if not inst["is_macro"] and not inst["is_fixed"]
    }

    G = build_weighted_graph(filtered_instances, data["hypergraph"], args.max_fanout)
    cluster_data, next_cluster_id, assigned_nodes = hierarchical_spectral_clustering(G, args.N)

    unclustered_nodes = [vid for vid in filtered_instances if vid not in assigned_nodes]
    if unclustered_nodes:
        subgraph = nx.Graph()
        subgraph.add_nodes_from(unclustered_nodes)
        for net, nodes in data["hypergraph"].items():
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    u, v = nodes[i], nodes[j]
                    if u in unclustered_nodes and v in unclustered_nodes:
                        if subgraph.has_edge(u, v):
                            subgraph[u][v]["weight"] += 1
                        else:
                            subgraph.add_edge(u, v, weight=1)

        reclustered_data, _, sub_assigned = hierarchical_spectral_clustering(
            subgraph, args.N, level=1, base_cluster_id=next_cluster_id)
        cluster_data.extend(reclustered_data)
        assigned_nodes.update(sub_assigned)

    all_levels, hierarchy_mapping = recursive_hierarchical_clustering(cluster_data, data["hypergraph"], args.N)

    all_explanations = {}
    for level, cluster_map in hierarchy_mapping.items():
        cluster_data_flat = [
            {"node": node, "cluster": cid}
            for cid, nodes in cluster_map.items()
            for node in nodes
        ]
        all_explanations[f"level_{level}"] = analyze_cluster_connectivity(cluster_data_flat, data["hypergraph"])

    output_placement = f"{args.design}_placement_clusters.json"
    print(f"[i] Writing placement clusters to: {output_placement}")
    with open(output_placement, "w") as f:
        json.dump(all_levels, f, indent=2)
    output_connectivity = f"{args.design}_cluster_connectivity_explanation.json"
    print(f"[i] Writing connectivity explanation to: {output_connectivity}")
    with open(output_connectivity, "w") as f:
        json.dump(all_explanations, f, indent=2)
    output_hierarchy = f"{args.design}_hierarchy.json"
    print(f"[i] Writing hierarchy to: {output_hierarchy}")
    with open(output_hierarchy, "w") as f:
        json.dump(all_levels, f, indent=2)

    # Save hierarchy to level-0 node mapping as a separate file
    hierarchy_flat_output = f"{args.design}_hierarchy_cluster.json"
    print(f"[i] Writing flat hierarchy node map to: {hierarchy_flat_output}")
    with open(hierarchy_flat_output, "w") as f:
        flat_map = {
            f"level_{level}": {
                str(cid): sorted(list(nodes)) for cid, nodes in cluster_map.items()
            } for level, cluster_map in hierarchy_mapping.items()
        }
        json.dump(flat_map, f, indent=2)

    for level_info in all_levels:
        level = level_info["level"]
        num_clusters = len(set(entry["cluster"] for entry in level_info["clusters"]))
        num_nodes = len(set(entry["node"] for entry in level_info["clusters"]))
        print(f"Level {level} → {num_nodes} nodes → {num_clusters} clusters")

    expected_nodes = set(filtered_instances.keys())
    missing_nodes = sorted(expected_nodes - assigned_nodes)
    if missing_nodes:
        print("[❌] ERROR: The following nodes were not assigned to any cluster:")
        print(missing_nodes)
    else:
        print("[✓] All eligible instances were assigned to clusters.")


if __name__ == "__main__":
    args = parse_arguments()
    filepath = f"{args.design}.pkl"
    main(filepath, args)
