# Author information
AUTHOR := Labriji Saad

# Default target when no arguments are provided to make
.DEFAULT_GOAL := help

# Run Jupyter Lab - starts Jupyter Lab to allow for interactive development
jupy:
	@echo "Starting Jupyter Lab..."
	@jupyter lab

# Run Kedro pipelines - executes the main pipeline defined in your Kedro project
run:
	@echo "Running Kedro pipeline..."
	@kedro run

# Run Kedro Viz - launches Kedro's visualization tool to view the pipeline structure
viz:
	@echo "Running Kedro Viz..."
	@kedro viz run

# Run Kedro Viz in autoreload mode - automatically refreshes the visualization when changes are detected
autoviz:
	@echo "Running Kedro Viz in autoreload mode..."
	@kedro viz run --autoreload

# Build Docker image for the project - creates a Docker image based on your Kedro project's specifications
build:
	@echo "Building Docker image..."
	@kedro docker build

# Run Kedro project inside a Docker container - executes the project within a Docker container
dockerun:
	@echo "Running Kedro project in Docker..."
	@kedro docker run

# Display help with available make targets
help:
	@echo Available targets:
	@echo   make jupy      - Activate the virtual environment and run Jupyter Lab
	@echo   make run       - Run Kedro pipelines
	@echo   make viz       - Run Kedro Viz
	@echo   make autoviz   - Run Kedro Viz in autoreload mode
	@echo   make build     - Build Docker image for the project
	@echo   make dockerun  - Run Kedro project inside a Docker container
	@echo Author: $(AUTHOR)