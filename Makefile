# Variables
VENV_NAME := venv
DATA_RAW_DIR := data/raw
DATA_PROCESSED_DIR := data/processed
DATA_EXTERNAL_DIR := data/external
NOTEBOOKS_DIR := notebooks
DOCS_DIR := docs
README_FILE := README.md
CONFIG_FILE := config.yaml
ENV_FILE := .env
GITIGNORE_FILE := .gitignore
REQUIREMENTS_FILE := requirements.txt
GITKEEP_FILE := .gitkeep
AUTHOR := labriji saad

# Default target
.DEFAULT_GOAL := help

# Update dependencies in the virtual environment
update:
	@$(VENV_ACTIVATE) && python.exe -m pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)
	@echo ">>>>>> Dependencies updated <<<<<<"

# Activate the virtual environment and run Jupyter Lab
jupyter:
	@$(VENV_ACTIVATE) && jupyter lab
	@echo ">>>>>> Jupyter Lab is running <<<<<<"

# Clean up the virtual environment and generated files
clean:
	@$(DELETE_CMD) $(VENV_NAME)
	@echo ">>>>>> Cleaned up environment <<<<<<"

# run Kedro pipelines 
run:
	@kedro run

# run Kedro Viz
viz:
	@kedro viz run

# Display available make targets
help:
	@echo Available targets:
	@echo   make update                                           - Update dependencies in the virtual environment
	@echo   make clean                                            - Clean up the virtual environment and generated files
	@echo   make jupyter                                          - Activate the virtual environment and run Jupyter Lab
	@echo Author: $(AUTHOR)