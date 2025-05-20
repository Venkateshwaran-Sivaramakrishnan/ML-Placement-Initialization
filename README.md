# ML-Placement-Initialization
ML-based placement initialization.

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
