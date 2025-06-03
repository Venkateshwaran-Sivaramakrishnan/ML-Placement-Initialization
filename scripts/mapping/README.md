# **Dataset Generation**

#### Objective:
Generate cluster-wise information about nodes and convert it into a format suitable for model inference.

This process involves the following steps:
1. Compute the area of superclusters and sort them.
2. Build internal node connectivity using shared net information.
3. Extract IO pin connectivity and assign regions accordingly.
4. Assign room types (T) to individual nodes and child clusters.
5. Apply size binning (S) based on calculated area.
6. Generate the adjacency matrix (A).
7. Output the final `.npy` file for inference.

---

#### Input Files:
1. Hypergraph text file: `{design}_{tech}.txt`
2. Cluster hierarchy JSON file: `{design}_hierarchy.json`

---

#### Output Files:
The full process in `run_full_hierarchy_pipeline.py` internally executes the following scripts, which produce these intermediate files:

1. From `compute_hierarcy_area.py`
``` bash
> level_cluster_map_unsorted.json
> cluster_area.json
> level_cluster_map_sorted.json
```

2. From `build_cluster_netlist.py`
``` bash
> cluster_netlists.json
```

3. From `instance_pin_boundary_map.py`
``` bash
> instance_pin_boundary_map.json
> cluster_boxes_map.json
```

4. From `compute_hierarchy_connectivity.py`
``` bash
> hierarchy_connectivity.json
> cluster_tensor_data.npy
```

---
#### Run the following command to implement the entire flow:


``` bash
python run_full_hierarchy_pipeline.py --design gcd --tech ihp-sg13g2
```
---
>*To check out what one data point would look like run the following script after running the entire flow*
```bash
python data_read.py
