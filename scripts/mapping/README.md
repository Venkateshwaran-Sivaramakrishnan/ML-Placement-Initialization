# **Dataset Generation**

## Objective

This module prepares hierarchical VLSI design data—including area, connectivity, and adjacency—for use as input to ML models such as MaskPLAN or Graph2Plan.

The pipeline performs the following steps:

1. Compute area of clustered nodes across hierarchy levels and sort them
2. Extract internal node connectivity using shared net information
3. Build I/O pin connectivity and assign region annotations
4. Assign room types (T) to each node and child cluster
5. Apply area-based binning to estimate room sizes (S)
6. Generate room adjacency matrix (A)
7. Save final input data as a `.npy` file suitable for model inference

---

## Required Inputs

Place the following files in the root of this subdirectory:

- `{design}_{tech}.txt`: Hypergraph file containing netlist and placement information
- `{design}_hierarchy.json`: JSON file defining the level-wise cluster structure of the design

> For example, when generating data for the GCD design using the ihp-sg13g2 technology node, ensure that the following input files are available in the working directory: 
> * `gcd_ihp-sg13g2.txt`
> * `gcd_hierarchy.json`
---

##Required Supporting Scripts

In addition to the input files above, the following Python scripts **must be present** in the working directory:

- `node_geometry.py`  
- `extractor.py`  
- `compute_hierarchy_area.py`  
- `build_cluster_netlist.py`  
- `instance_pin_boundary_map.py`  
- `compute_hierarchy_connectivity.py`

These scripts are invoked by the main pipeline and must be accessible at runtime.

---
## Output Files

The complete pipeline is run via the script `run_full_hierarchy_pipeline.py`. Internally, it calls the following scripts in order, each producing intermediate outputs:

### 1. `compute_hierarchy_area.py`
- `cluster_area.json`: Area of each cluster at each hierarchy level
- `level_cluster_map_unsorted.json`: Raw cluster-to-node map
- `level_cluster_map_sorted.json`: Area-ranked cluster-to-node map

### 2. `build_cluster_netlist.py`
- `cluster_netlists.json`: Cluster-level net connectivity information

### 3. `instance_pin_boundary_map.py`
- `instance_pin_boundary_map.json`: Maps I/O pins to standard cells
- `cluster_boxes_map.json`: Cluster bounding box coordinates

### 4. `compute_hierarchy_connectivity.py`
- `hierarchy_connectivity.json`: Enriched cluster connectivity info with area, connection counts, and internal links
- `cluster_tensor_data.npy`: Final tensor formatted for model inference

---

## How to Run: 

To execute the full preprocessing pipeline **from the command line**, use:

```bash
python run_full_hierarchy_pipeline.py --design gcd --tech ihp-sg13g2
```
> **Note:** Replace `gcd` and `ihp-sg13g2` with the approporiate design and tech node

---
To call the pipeline from within another Python script **as a function**, use:

```bash
from run_full_hierarchy_pipeline import run_full_hierarchy_pipeline

design = "gcd"
tech = "ihp-sg13g2"
run_full_hierarchy_pipeline(design, tech)

```
---
## Visualizing Output
To inspect one processed data sample from the final output, run:
```bash
python data_read.py
```
This will print the shape, keys, and content of one example in the `.npy` file.
