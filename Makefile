AUTHOR := Labriji Saad

# Default target
.DEFAULT_GOAL := help

#  run Jupyter Lab
jupy:
	@jupyter lab

# run Kedro pipelines 
run:
	@kedro run

# run Kedro Viz
viz:
	@kedro viz run

# Display available make targets
help:
	@echo  Available targets:
	@echo    make jupy     - Activate the virtual environment and run Jupyter Lab
	@echo    make run      - Run Kedro pipelines
	@echo    make viz      - Run Kedro Viz
	@echo  Author: $(AUTHOR)