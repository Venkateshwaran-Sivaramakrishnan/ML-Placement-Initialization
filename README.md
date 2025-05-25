# ML-Placement-Initialization
ML-based placement initialization.

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

## MaskPLAN Inference

To run inference, please run:

```bash
uv run python -m Inference.MaskPLAN_Inference_iterate_vec_Single
```

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
