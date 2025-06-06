DESIGN ?= gcd
TECH_NODE ?= asap7
MAX_NODES ?= 8

CE ?= docker

OPENROAD = $(CE) run -v ./:/ml_placer --rm ghcr.io/udxs/ece260c-essential:main bash -c

ORFS_DIR = OpenROAD-flow-scripts/flow
CD_ORFS = cd $(ORFS_DIR)
CD_ORFS_CE = cd /ml_placer/$(ORFS_DIR)
SETUP_CE = $(CD_ORFS_CE) && PATH=/opt/oss-cad-suite/bin:/root/miniconda3/bin:$$PATH YOSYS_EXE=/opt/oss-cad-suite/bin/yosys OPENROAD_EXE=/usr/bin/openroad
DESIGN_DIR = ./designs/$(TECH_NODE)/$(DESIGN)
CD_BASE_DIR = $(CD_ORFS)/results/$(TECH_NODE)/$(DESIGN)/base
RUN_SCRIPT = $(CD_BASE_DIR) && time pixi run python ../../../../../../

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: pin_placement extract_hypergraph extract_results cluster

.pixi:
	pixi install

OpenROAD-flow-scripts: ## Clones ORFS to the repo via the docker container
	$(OPENROAD) "cd /ml_placer && /usr/bin/orfs_copy"

pin_placement: OpenROAD-flow-scripts ## Runs ORFS until the pin placement via docker container
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_2_place_iop"

extract_hypergraph: pin_placement ## Runs hypergraph extraction script
	$(OPENROAD) "$(SETUP_CE) openroad -python ../../scripts/hypergraph/python_read_design.py"

extract_results: .pixi pin_placement ## Extracts the results from the ORFS run so far
	$(RUN_SCRIPT)/scripts/clustering/extractor.py --design $(DESIGN) --tech $(TECH_NODE)

cluster: .pixi pin_placement ## Clusters the design
	$(RUN_SCRIPT)/scripts/clustering/cluster.py --design $(DESIGN) --N $(MAX_NODES)

generate_input: ## Generates .npy files for inference
	$(RUN_SCRIPT)/scripts/mapping/run_full_hierarchy_pipeline.py --design $(DESIGN) --tech $(TECH_NODE)

predict:
	pixi run python OpenROAD-flow-scripts/flow/results/$(TECH_NODE)/$(DESIGN)/base/cluster_tensor_data.npy OpenROAD-flow-scripts/flow/results/$(TECH_NODE)/$(DESIGN)/base/cluster_tensor_prediction.npy --par_L 0
