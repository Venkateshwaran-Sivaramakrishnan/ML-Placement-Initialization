DESIGN ?= gcd
TECH_NODE ?= asap7
MAX_NODES ?= 8
NO_PRED ?= 1

CE ?= docker

OPENROAD = $(CE) run --mount "type=bind,src=$(PWD),dst=/ml_placer" --rm ghcr.io/udxs/ece260c-essential:main bash -c

ORFS_DIR = OpenROAD-flow-scripts/flow
CD_ORFS = cd $(ORFS_DIR)
CD_ORFS_CE = cd /ml_placer/$(ORFS_DIR)
SETUP_CE = source /ml_placer/source_env.sh && $(CD_ORFS_CE) &&
DESIGN_DIR = designs/$(TECH_NODE)/$(DESIGN)
CD_BASE_DIR = $(CD_ORFS)/results/$(TECH_NODE)/$(DESIGN)/base
RUN_SCRIPT = $(CD_BASE_DIR) && time pixi run python ../../../../../../
REL_DIR = ../../../../../../
RESULT_DIR = $(PWD)/results/$(DESIGN)_$(TECH_NODE)

help: ## Prints help for targets with comments
	@echo "usage: DESIGN=<design> TECH_NODE=<tech> NO_PRED=<0|1> make ..."
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: pin_placement extract_hypergraph extract_results cluster generate_input predict map_prediction read_initial_placement finish_openroad

.pixi:
	pixi install

OpenROAD-flow-scripts: ## Clones ORFS
	git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git

pin_placement: OpenROAD-flow-scripts ## Runs ORFS until the pin placement via docker container
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_2_place_iop"

$(RESULT_DIR):
ifeq ($(NO_PRED), 1)
	mkdir -p results
	ln -s $(PWD)/database/$(DESIGN)_$(TECH_NODE) $(RESULT_DIR)
else
	mkdir -p $@
endif

extract_hypergraph: pin_placement $(RESULT_DIR) ## Runs hypergraph extraction script
	$(OPENROAD) "$(SETUP_CE) openroad -python ../../scripts/hypergraph/python_read_design.py -d $(DESIGN) -t $(TECH_NODE)"
	@cp OpenROAD-flow-scripts/flow/results/$(TECH_NODE)/$(DESIGN)/base/$(DESIGN)_$(TECH_NODE).txt $(RESULT_DIR)/

extract_results: .pixi pin_placement $(RESULT_DIR) ## Extracts the results from the ORFS run so far
	$(RUN_SCRIPT)/scripts/clustering/extractor.py --design $(DESIGN) --tech $(TECH_NODE) --output_dir $(RESULT_DIR)

cluster: .pixi pin_placement ## Clusters the design
ifeq ($(NO_PRED), 1)
	@echo "Skipping clustering..."
else
	$(RUN_SCRIPT)/scripts/clustering/cluster.py $(RESULT_DIR)/$(DESIGN).pkl --design $(DESIGN) --N $(MAX_NODES) --output_dir $(RESULT_DIR)
endif

generate_input: pin_placement ## Generates .npy files for inference
	cd $(RESULT_DIR) && pixi run python ../../scripts/mapping/run_full_hierarchy_pipeline.py --design $(DESIGN) --tech $(TECH_NODE)

predict: $(RESULT_DIR) generate_input ## Runs inference
ifeq ($(NO_PRED), 1)
	@echo "Skipping prediction..."
else
	pixi run python model/predict.py $(RESULT_DIR)/cluster_tensor_data.npy $(RESULT_DIR)/cluster_tensor_prediction.npy --par_L 0
endif

map_predictions: $(RESULT_DIR) predict ## Generate placement
ifneq ($(NO_PRED), 1)
	make predict
endif
	cd $(RESULT_DIR) && pixi run python ../../scripts/prediction/mapInference.py --design $(DESIGN)	

read_initial_placement: map_predictions
	@cp $(RESULT_DIR)/init_placement_test.txt $(ORFS_DIR)
	$(OPENROAD) "$(SETUP_CE) openroad -python ../../scripts/hypergraph/python_read_design.py -d $(DESIGN) -t $(TECH_NODE) --incremental 1"
	
finish_placement: read_initial_placement
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_5_place_dp"
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_3_place_gp.log $(RESULT_DIR)/3_3_place_gp.results.json
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_5_place_dp.json $(RESULT_DIR)/3_5_place_dp.results.json
	@tac $(RESULT_DIR)/3_3_place_gp.log | awk '/\[NesterovSolve\] Iter:/ { printf "# of Iterations: %s\n", $$3; exit}' | tee $(RESULT_DIR)/results.txt
	@awk '/detailedplace__route__wirelength__estimated/ {printf "Estimated Wirelength: %s um\n", $$2}' $(RESULT_DIR)/3_5_place_dp.json | tr -d ',' | tee -a $(RESULT_DIR)/results.txt

baseline: OpenROAD-flow-scripts $(RESULT_DIR)
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make clean_all && DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_5_place_dp"
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_3_place_gp.log $(RESULT_DIR)/3_3_place_gp.baseline.log
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_5_place_dp.json $(RESULT_DIR)/3_5_place_dp.baseline.json
	@tac $(RESULT_DIR)/3_3_place_gp.log | awk '/\[NesterovSolve\] Iter:/ { printf "# of Iterations: %s\n", $$3; exit}' | tee $(RESULT_DIR)/baseline.txt
	@awk '/detailedplace__route__wirelength__estimated/ {printf "Estimated Wirelength: %s um\n", $$2}' $(RESULT_DIR)/3_5_place_dp.json | tr -d ',' | tee -a $(RESULT_DIR)/baseline.txt
