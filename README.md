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
Ensure you have [pixi](https://pixi.sh/v0.47.0/) installed.
This will allow you to install the dependencies for the design.

```bash
# Installs python3.9 environment, all dependencies, CUDA support
pixi install

# Run this to enter the environment installed above
pixi shell
```

Ensure you have [docker](https://www.docker.com/).
This will allow you to run the OpenROAD side of things for the flow.

These scripts have been extensively tested on Linux systems and, to a limited extent, on WSL.

Please refer to this [docker desktop on WSL installation guide](https://github.com/VenkateshwaranSivaramakrishnan/ML-Based-Placement-Initialization/blob/main/WSL%20%7C%20Docker%20Desktop%20Installation%20Guide.md) for Windows. 

MacOS might work but hasn't been rigorously tested.

---

## Inference

**Note:** For peer reproducibility, we provide pre-inferred data for the test designs and integrate it into our flow, for individuals/teams not having access to GPU compute. Hypergraph extraction, clustering, mapping, and post-inference mapping are executed using CPU compute on the fly.

The MaskPLAN Inference is tailored to meet placement requirements.

**Flow:** 
1. Run OpenROAD upto 3_2_place_iop
2. Generate Hypergraph using python_read_design.py
3. Run extractor.py
4. Run cluster.py
5. Model Inference 

View the documentation with this command:

```bash
DESIGN={orfs design} TECH_NODE={orfs tech} NO_PRED={0|1} CE={docker|podman} make run
```

Suppose we want to run our flow for `gcd` on `nangate45`, and don't want to run any predictions.
Then, we could first generate baseline files for comparison with `DESIGN=gcd TECH=nangate45 NO_PRED=1 make baseline`.
Then to run with the new flow, we could run `DESIGN=gcd TECH_NODE=nangate45 NO_PRED=1 make run`.

The final results and all artifacts generated by the flow is located in `results/{design}_{tech}/`

**Note** Only the designs in `database/` support no prediction runs.

#### Input
<p align="center">
  <img src="https://github.com/user-attachments/assets/80f9eb62-fd44-4ab6-837e-f6c6d5adc625" width="200"/>
</p>

#### Output
<p align="center">
  <img src="https://github.com/user-attachments/assets/978e778f-a05d-4978-baf3-c579526cc356" width="400"/>
</p>

### Custom Inference (requires GPU)

---

## Improvements
1. Currently developing a stitching flow to assemble cluster-level results into a unified floorplan.
2. Simultaneously exploring advanced mapping techniques to enhance overall QoR.
---

## Citation
```
@inproceedings{zhang2024maskplan,
  title={MaskPLAN: Masked Generative Layout Planning from Partial Input},
  author={Zhang, Hang and Savov, Anton and Dillenburger, Benjamin},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={8964--8973},
  year={2024}
}
```
