DESIGN ?= gcd
TECH_NODE ?= asap7
MAX_NODES ?= 8
NO_PRED ?= 1

CE ?= docker

OPENROAD = $(CE) run --mount "type=bind,src=$(PWD),dst=/ml_placer" --rm ghcr.io/udxs/ece260c-essential:main bash -c

ORFS_DIR = OpenROAD-flow-scripts/flow
DESIGN_DIR = designs/$(TECH_NODE)/$(DESIGN)
DESIGN_RESULTS_DIR = $(ORFS_DIR)/results/$(TECH_NODE)/$(DESIGN)/base
CD_ORFS = cd $(ORFS_DIR)
CD_ORFS_CE = cd /ml_placer/$(ORFS_DIR)
SETUP_CE = source /ml_placer/source_env.sh && $(CD_ORFS_CE) &&
CD_DESIGN_RESULTS_DIR = cd $(DESIGN_RESULTS_DIR)
RUN_SCRIPT = $(CD_DESIGN_RESULTS_DIR) && time pixi run python ../../../../../../
RESULT_DIR = $(PWD)/results/$(DESIGN)_$(TECH_NODE)
MAKE_LOG = $(RESULT_DIR)/make.log
LOG = tee -a $(MAKE_LOG)

help: ## Prints help for targets with comments
	@echo "usage: DESIGN=<design> TECH_NODE=<tech> NO_PRED=<0|1> make ..."
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(RESULT_DIR):
	mkdir -p $@
	@date > "$(MAKE_LOG)"

.pixi:
	pixi install

OpenROAD-flow-scripts:
	git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git

start_floorplan: $(DESIGN_RESULTS_DIR)/3_2_place_iop.odb $(DESIGN_RESULTS_DIR)/2_floorplan.sdc ## Runs IO placement
extract_hypergraph: $(RESULT_DIR)/$(DESIGN)_$(TECH_NODE).txt ## Runs hypergraph extraction script
extract_results: $(RESULT_DIR)/$(DESIGN).pkl $(RESULT_DIR)/$(DESIGN).json ## Extracts the results from the ORFS run so far
cluster: $(RESULT_DIR)/$(DESIGN)_placement_clusters.json $(RESULT_DIR)/$(DESIGN)_cluster_connectivity_explanation.json $(RESULT_DIR)/$(DESIGN)_hierarchy.json $(RESULT_DIR)/$(DESIGN)_hierarchy_cluster.json ## Clusters the design
generate_input: $(RESULT_DIR)/cluster_area.json $(RESULT_DIR)/level_cluster_map_unsorted.json $(RESULT_DIR)/level_cluster_map_sorted.json $(RESULT_DIR)/cluster_netlists.json $(RESULT_DIR)/instance_pin_boundary_map.json $(RESULT_DIR)/cluster_boxes_map.json $(RESULT_DIR)/hierarchy_connectivity.json $(RESULT_DIR)/cluster_tensor_data.npy ## Generates .npy files for inference
predict: $(RESULT_DIR)/cluster_tensor_prediction.npy ## Runs inference
map_predictions: $(RESULT_DIR)/init_placement_test.txt ## Generate placement
read_predictions: $(DESIGN_RESULTS_DIR)/3_3_place_gp.odb ## Generate incremental placement db
finish_placement: $(RESULT_DIR)/results.txt ## Run rest of placement and get HPWL and iter count

run: finish_placement ## Run entire flow

baseline: $(RESULT_DIR)/baseline.txt ## Run ORFS without our flow to get baseline metrics

all: baseline run ## Runs both the baseline and the main flow

clean: ## Deletes results directory (should re-trigger most targets)
	rm -rf $(RESULT_DIR)

clean_orfs: ## Deletes all placement runs for a target in ORFS
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make clean_place" 

# Placement flow
# 0. Generate baseline results?
# 1. Run up to pin placement
# 2. Generate the hypergraph for global placement
# 3. Get the information from ORFS
# 4. Construct the clusters
# 5. Generate the inputs from clusters
# 6. Run prediction
# 7. Map our predictions
# 8. Read initial placements in
# 9. Run the rest of placement

# Step 1 - Run ORFS up to I/O placement
$(DESIGN_RESULTS_DIR)/3_2_place_iop.odb $(DESIGN_RESULTS_DIR)/2_floorplan.sdc: OpenROAD-flow-scripts
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_2_place_iop" | $(LOG)

# Step 2 - Generate the hypergraph
$(RESULT_DIR)/$(DESIGN)_$(TECH_NODE).txt: $(DESIGN_RESULTS_DIR)/3_2_place_iop.odb $(DESIGN_RESULTS_DIR)/2_floorplan.sdc $(RESULT_DIR)
	$(OPENROAD) "$(SETUP_CE) openroad -python ../../scripts/hypergraph/python_read_design.py -d $(DESIGN) -t $(TECH_NODE)" | $(LOG)
	@cp $(DESIGN_RESULTS_DIR)/$(DESIGN)_$(TECH_NODE).txt $@

# Step 3 - Extract design information from the hypergraph
$(RESULT_DIR)/$(DESIGN).pkl $(RESULT_DIR)/$(DESIGN).json: .pixi $(RESULT_DIR)/$(DESIGN)_$(TECH_NODE).txt
	$(RUN_SCRIPT)/scripts/clustering/extractor.py --design $(DESIGN) --tech $(TECH_NODE) --output_dir $(RESULT_DIR) | $(LOG)

# Step 4 - Create the clusters
$(RESULT_DIR)/$(DESIGN)_placement_clusters.json $(RESULT_DIR)/$(DESIGN)_cluster_connectivity_explanation.json $(RESULT_DIR)/$(DESIGN)_hierarchy.json $(RESULT_DIR)/$(DESIGN)_hierarchy_cluster.json: $(RESULT_DIR)/$(DESIGN).pkl
	$(RUN_SCRIPT)/scripts/clustering/cluster.py $(RESULT_DIR)/$(DESIGN).pkl --design $(DESIGN) --N $(MAX_NODES) --output_dir $(RESULT_DIR) | $(LOG)

# Step 5 - Create the input file for prediction
$(RESULT_DIR)/cluster_area.json $(RESULT_DIR)/level_cluster_map_unsorted.json $(RESULT_DIR)/level_cluster_map_sorted.json $(RESULT_DIR)/cluster_netlists.json $(RESULT_DIR)/instance_pin_boundary_map.json $(RESULT_DIR)/cluster_boxes_map.json $(RESULT_DIR)/hierarchy_connectivity.json $(RESULT_DIR)/cluster_tensor_data.npy: $(RESULT_DIR)/$(DESIGN)_$(TECH_NODE).txt $(RESULT_DIR)/$(DESIGN)_hierarchy.json
	cd $(RESULT_DIR) && pixi run python ../../scripts/mapping/run_full_hierarchy_pipeline.py --design $(DESIGN) --tech $(TECH_NODE) | $(LOG)

# Step 6 - Run our predictions. If we are skipping predictions, copy the prediction file from a ground truth.
$(RESULT_DIR)/cluster_tensor_prediction.npy: $(RESULT_DIR)/cluster_tensor_data.npy
ifeq ($(NO_PRED), 1)
	cp database/$(DESIGN)_$(TECH_NODE)/cluster_tensor_prediction.npy $(RESULT_DIR)/cluster_tensor_prediction.npy
	@echo "Skipping inference..." | $(LOG)
else
	pixi run python model/predict.py $(RESULT_DIR)/cluster_tensor_data.npy $(RESULT_DIR)/cluster_tensor_prediction.npy --par_L 0 --model Large | $(LOG)
endif

# Step 7 - Map our predictions
$(RESULT_DIR)/init_placement_test.txt $(ORFS_DIR)/init_placement_test.txt: $(RESULT_DIR)/$(DESIGN).pkl $(RESULT_DIR)/$(DESIGN).json $(RESULT_DIR)/cluster_tensor_prediction.npy
	cd $(RESULT_DIR) && pixi run python ../../scripts/prediction/mapInference.py --design $(DESIGN)	| $(LOG)
	@cp $(RESULT_DIR)/init_placement_test.txt $(ORFS_DIR)/init_placement_test.txt

# Step 8 - Read our initial placements back in to OR
$(DESIGN_RESULTS_DIR)/3_3_place_gp.odb: $(ORFS_DIR)/init_placement_test.txt	
	$(OPENROAD) "$(SETUP_CE) rm -rf results/$(TECH_NODE)/$(DESIGN)/base/3_5_*; openroad -python ../../scripts/hypergraph/python_read_design.py -d $(DESIGN) -t $(TECH_NODE) --incremental 1" | tee $(RESULT_DIR)/global_placement.log | $(LOG)
	
# Step 9 - Run rest of placement
$(RESULT_DIR)/results.txt: $(DESIGN_RESULTS_DIR)/3_3_place_gp.odb
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_5_place_dp" | tee $(RESULT_DIR)/final_placement.log
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_5_place_dp.json $(RESULT_DIR)/3_5_place_dp.results.json
	@tac $(RESULT_DIR)/final_placement.log | awk '/final/ {f=1;next} f { printf "# of Iterations: %s\n", $$1; exit}' | tee $(RESULT_DIR)/results.txt
	@tac $(RESULT_DIR)/global_placement.log | awk '/\[NesterovSolve\] Iter:/ { printf "# of Global Placement Iterations: %s\n", $$3; exit}' | tee -a $(RESULT_DIR)/results.txt
	@awk '/detailedplace__route__wirelength__estimated/ {printf "Estimated Wirelength: %s um\n", $$2}' $(RESULT_DIR)/3_5_place_dp.results.json | tr -d ',' | tee -a $(RESULT_DIR)/results.txt

# Step 0 - Run baseline
$(RESULT_DIR)/baseline.txt: OpenROAD-flow-scripts $(RESULT_DIR)
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make clean_place && DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make 3_5_place_dp" | tee $(RESULT_DIR)/baseline_placement.log
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_3_place_gp.log $(RESULT_DIR)/3_3_place_gp.baseline.log
	@cp $(ORFS_DIR)/logs/$(TECH_NODE)/$(DESIGN)/base/3_5_place_dp.json $(RESULT_DIR)/3_5_place_dp.baseline.json
	@tac $(RESULT_DIR)/baseline_placement.log | awk '/final/ {f=1;next} f { printf "# of Detailed Placement Iterations: %s\n", $$1; exit}' | tee $(RESULT_DIR)/baseline.txt
	@tac $(RESULT_DIR)/3_3_place_gp.baseline.log | awk '/\[NesterovSolve\] Iter:/ { printf "# of Global Placement Iterations: %s\n", $$3; exit}' | tee -a $(RESULT_DIR)/baseline.txt
	@awk '/detailedplace__route__wirelength__estimated/ {printf "Estimated Wirelength: %s um\n", $$2}' $(RESULT_DIR)/3_5_place_dp.baseline.json | tr -d ',' | tee -a $(RESULT_DIR)/baseline.txt
	$(OPENROAD) "$(SETUP_CE) DESIGN_CONFIG=$(DESIGN_DIR)/config.mk make clean_place"
