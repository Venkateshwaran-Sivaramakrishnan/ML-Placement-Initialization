from compute_hierarchy_area import compute_hierarchy_area
from build_cluster_netlists import build_cluster_netlists
from instance_pin_boundary_map import build_instance_pin_boundary_and_boxes
from compute_hierarchy_connectivity import compute_hierarchy_connectivity

import argparse

def run_full_hierarchy_pipeline(design = "gcd", tech = "ihp-sg13g2"):

    print("Step 1: Compute hierarchy area and cluster maps...")
    compute_hierarchy_area(design, tech)

    print("Step 2: Build cluster netlists...")
    build_cluster_netlists(design, tech)

    print("Step 3: Build instance pin boundary and cluster boxes...")
    build_instance_pin_boundary_and_boxes(design, tech)

    print("Step 4: Compute hierarchy connectivity and save .npy...")
    compute_hierarchy_connectivity(design, tech)

    print("✅ All steps completed!")



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
    run_full_hierarchy_pipeline(design, tech)