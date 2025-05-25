# **Dataset Generation**
### **Step 1:**  
#### Objective:
1.   Generate information about nodes in cluster
2.   Area of super clusters and sorting

#### Input Files:
> Hypergraph text file - eg.: `ibex_nangate.txt`

> Cluster Hierarchy json file - `hierarchy.json`

#### Output Files:

``` bash
> level_cluster_map_unsorted.json
> cluster_area.json
> level_cluster_map_sorted.json
```

#### Run the following command to implement step 1:

``` bash
python .\compute_hierarchy_area.py --design ibex --tech nangate45
```

Change the attributes appropriately

### **Step 2:**
#### Objective
1. Assign room types (T) for nodes and child clusters
2. Apply size binning (S) based on computed area
3. Generate Adjacenecy Matrix (A)
2. Generate `.npy` file for inference

#### Inputs:
```bash
> level_cluster_map_unsorted.json
> cluster_area.json
```

#### Outputs:
```bash
> hierarchy_connectivity.json
> cluster_tensor_data.npy
```

#### Run the following command to implement step 2:

```bash
python .\compute_hierarchy_connectivity.py --design ibex --tech nangate45
```
---
>*To check out what one data point would look like run the following script*
```bash
python data_read.py
```
