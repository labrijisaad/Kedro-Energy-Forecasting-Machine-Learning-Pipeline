AUTHOR := Labriji Saad

# Default target
.DEFAULT_GOAL := help

# run Jupyter Lab
jupy:
	@jupyter lab

# run Kedro pipelines 
run:
	@kedro run

# run Kedro Viz
viz:
	@kedro viz run

# run Kedro Viz in autoreload mode
autoviz:
	@kedro viz run --autoreload

# Display available make targets
help:
	@echo  Available targets:
	@echo    make jupy      - Activate the virtual environment and run Jupyter Lab
	@echo    make run       - Run Kedro pipelines
	@echo    make viz       - Run Kedro Viz
	@echo    make autoviz   - Run Kedro Viz in autoreload mode
	@echo  Author: $(AUTHOR)