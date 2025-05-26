# ML-Based Placement Initialization

This project presents an adaptation of **ML-based architectural layout generation** techniques to the problem of **VLSI placement initialization**, using principles of **transfer learning**. Specifically, we explore and build upon prior work in architectural layout generation to inform the development of effective placement initialization strategies for the OpenROAD placement flow. 

---

## Explored Works: 

We evaluated the following works which addresses floorplan generation using machine learning:

| Model | Description |
|-------|-------------|
| **[MaskPLAN](https://github.com/HangZhangZ/MaskPLAN)** | Masked generative layout planning using graph-structured dynamic masked autoencoders (CVPR 2024) [[paper](https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_MaskPLAN_Masked_Generative_Layout_Planning_from_Partial_Input_CVPR_2024_paper.html)] |
| **[Graph2Plan](https://github.com/HanHan55/Graph2plan)** | Floorplan generation from layout graphs using GCN-based message passing [[paper](https://arxiv.org/abs/2004.13204)] |
| **[iPLAN](https://github.com/realcrane/iPLAN-Interactive-and-Procedural-Layout-Planning)** | Interactive layout design framework leveraging procedural generation [[paper](https://arxiv.org/pdf/2203.14412)] |
| **[GPLAN](https://arxiv.org/pdf/2008.01803)** | Constraint-based dimensioned floorplan generation for adjacency-constrained spaces |
| **[HouseGAN](https://github.com/ennauata/housegan)** | GAN-based architectural layout generation |
| **[GNN-FP](https://github.com/mo7amed7assan1911/Floor_Plan_Generation_using_GNNs)** | Floorplan prediction using graph neural networks |


**MaskPLAN** emerged as the most suitable foundation for our placement initialization problem.

---

## Why MaskPLAN? 

Among the models evaluated, **MaskPLAN** was selected for adaptation to VLSI due to its capability to infer complete layouts from **partial or masked inputs**, a valuable feature when some placement details are not predefined.

---

## MaskPLAN: Overview

MaskPLAN employs a **Graph-structured Dynamic Masked Autoencoder (GDMAE)** architecture. It includes five parallel transformer modules, each responsible for learning different layout attributes:

- **T** — Room Type  
- **L** — Room Location  
- **S** — Room Size  
- **A** — Adjacency  
- **R** — Room Region  
- Boundary Image  
- Front Door Position  

---
## Challenges and Solutions: 


| Challenge | Resolution |
|----------|------------|
| Upto 8 rooms (7 types) can be generated | Limit layout prediction to **8 nodes (max) by clustering**|
| Architectural ≠ Placement Initialization constraints | Perform **domain-specific feature mapping** |
| Room Location unknown in Placement Initialization | Use **partial inputs** (omit L) |


---

## Adapting MaskPLAN to Initial Placement


### 1. Clustering Strategy

To convert the flat VLSI netlist into higher-order layout entities:

- The clustering process groups instances (cells) based on **netlist connectivity** to maintain spatial locality and logical grouping.
- Builds a weighted graph from instance-level net connectivity, filtering high-fanout nets.
- **Hierarchical clustering**: Applies spectral clustering recursively to limit cluster size to ≤ N nodes.
- Forms supergraphs where each node represents a cluster from the previous level.
- Clusters supergraphs hierarchically to build a multi-level cluster hierarchy.
- Generates connectivity explanations and flat mappings for interpretability and debugging.
- **Maximum cluster size** is limited to **8**, aligning with MaskPLAN's capacity to generate up to 8 rooms.


### 2. Feature Mapping Between Domains

| Architectural Feature (MaskPLAN) | VLSI Equivalent |
|----------------------------------|-----------------|
| **T** (Type) | Clustered node or sub-cluster, categorized by area and connectivity |
| **S** (Size) | Area of a cell or sum of areas in a sub-cluster |
| **A** (Adjacency) | Connectivity between nodes/clusters from netlist (hypergraph) |
| **R** (Region) | Estimated based on proximity to I/O pins |
| **L** (Location) | *Unavailable* in placement initialization (replaced by partial input handling) |

> Note: **L** is intentionally omitted, leveraging MaskPLAN’s partial input capability.

---


## Dependencies
Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
Conda is used solely to install CUDA 11 and CUDNN 8.
If you have CUDA 11 and CUDNN 8 installed on the system you can safely ignore the `conda` commands.
To get all the dependencies, please run the following in order:

```bash
conda create -n MLPlacement python=3.9
conda activate MLPlacement
conda install -c conda-forge cudatoolkit==11.8 cudnn==8.2.1.32

# Run only this if you have CUDA installed already
uv sync --no-managed-python

# You do not need to activate the environment again after running uv sync.
conda deactivate MLPlacement

# Source OpenROAD variables
source OpenROAD-flow-scripts/env.sh
```

## Inference

The MaskPLAN Inference is taylored to meet placement requirements.

To run complete OpenROAD flow:

Run OpenROAD upto 3_2_place_iop -->  Generate Hypergraph using python_read_design.py --> Run extractor.py --> Run cluster.py --> Model Inference 

```bash
python run.py -d {design} -t {tech} -N {cluster_size}

Example:
python run.py -d ibex -t nangate45 -N 8
```

To run single inference:

```bash
cd Inference
uv run python -m Inference.MaskPLAN_Inference_iterate_vec_Single --model Large --par_L 0 --par_R 0
```

#### Input
<p align="center">
  <img src="https://github.com/user-attachments/assets/80f9eb62-fd44-4ab6-837e-f6c6d5adc625" width="200"/>
</p>

#### Output
<p align="center">
  <img src="https://github.com/user-attachments/assets/978e778f-a05d-4978-baf3-c579526cc356" width="400"/>
</p>

### extractor.py
```bash
python extractor.py --design {design_name} --tech {tech_node}

Output:
{design}.pkl
{design}.json

Example:
python extractor.py --design ibex --tech nangate45
```
### cluster.py
```bash
python cluster.py --design {design_name} --N {cluster_size} --cluster_stop_length {cluster_stop_length}

Output:
{design}_instance_cluster_map.json
{design}_hierarchy.json
{design}_instance_cluster_plot.svg
{design}_hierarchy_tree.svg

Example:
python cluster.py --design ibex --N 5 --cluster_stop_length 10
```
