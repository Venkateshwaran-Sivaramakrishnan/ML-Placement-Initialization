import json
from collections import defaultdict
from extractor import DesignParser
import argparse

def build_cluster_netlists(design = "gcd", tech = "ihp-sg13g2"):
    design_txt = f"{design}_{tech}.txt"
    # Load design and cluster maps
    with open("level_cluster_map_unsorted.json", "r") as f:
        level_cluster_map = json.load(f)

    # Initialize design parser
    design = DesignParser(design_txt)  # Update filename as needed

    # Build node-to-nets map for level 0
    node_to_nets = defaultdict(set)
    for net_id, nodes in design.hypergraph.items():
        for node in nodes:
            node_to_nets[str(node)].add(int(net_id))

    def get_leaf_nodes(node, level, level_cluster_map):
        """Recursively get all level-0 descendants for a supernode."""
        if level == 0:
            return [int(node)] if isinstance(node, (int, str)) and str(node).isdigit() else []
        node_str = str(node)
        # Find the cluster at level-1 that contains this node
        for cluster_id, node_list in level_cluster_map[level-1].items():
            node_list_str = [str(n) for n in node_list]
            if node_str in node_list_str:
                # This node is a supernode at level-1, so get its children
                leafs = []
                for child in node_list:
                    leafs.extend(get_leaf_nodes(child, level-1, level_cluster_map))
                return leafs
        # If not found, treat as leaf (shouldn't happen)
        return []

    # Build cluster netlists for all levels
    cluster_netlists = {}

    # Level 0: direct node-to-nets
    level_0_map = level_cluster_map[0]
    cluster_netlists["level_0"] = {}
    for cluster_id, node_list in level_0_map.items():
        cluster_netlists["level_0"][str(cluster_id)] = {}
        for node_id in node_list:
            nets = list(node_to_nets.get(str(node_id), set()))
            cluster_netlists["level_0"][str(cluster_id)][str(node_id)] = nets

    # Higher levels: for each cluster, for each supernode, union nets of all nodes in the corresponding level 0 cluster
    for level in range(1, len(level_cluster_map)):
        level_key = f"level_{level}"
        cluster_netlists[level_key] = {}
        level_map = level_cluster_map[level]
        for cluster_id, node_list in level_map.items():
            cluster_netlists[level_key][str(cluster_id)] = {}
            for supernode in node_list:
                # Extract the numeric part of the supernode name
                if isinstance(supernode, str) and "N" in supernode:
                    cluster_num = supernode.split("N")[-1]
                else:
                    cluster_num = str(supernode)
                # Get all nets in level 0's cluster with this number
                nets_union = set()
                if cluster_num in cluster_netlists["level_0"]:
                    for nets in cluster_netlists["level_0"][cluster_num].values():
                        nets_union.update(nets)
                cluster_netlists[level_key][str(cluster_id)][str(supernode)] = list(nets_union)

    # Dump to JSON
    with open("cluster_netlists.json", "w") as f:
        json.dump(cluster_netlists, f, indent=2)

    print("✅ Dumped cluster netlists to cluster_netlists.json")

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
    build_cluster_netlists(design, tech)