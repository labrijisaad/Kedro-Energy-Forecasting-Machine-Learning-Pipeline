# `Kedro` Machine Learning Pipeline 🏯

<p align="center">
  <img src="https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/b63b891c-acf0-423e-8ca0-d8baa74a51e6" width="70%" />
</p>

<blockquote align="center">
  <i>"This DALL-E generated image, within Japan, Kedro orchestrates the rhythm of renewable insights amidst the choreography of data and predictions."</i>
</blockquote>

## 📘 Introduction

In this project, I challenged myself to transform notebook-based code for model training into a Kedro pipeline. The idea is to create modular, simple-to-train pipelines following the best MLOPS practices, to simplify the deployment of ML models.

## 🎯 Project Goals

The objective was :
- Refine a raw energy dataset into a polished series of features ready for forecasting.
- Deploy daily and monthly prediction models grounded in historical patterns.
- Adopt the Kedro framework to produce reproducible, modular, and scalable workflows.

## 🧩 Project Workflow

The `src` directory is the essence, with each component neatly arranged in a Kedro pipeline:

- **Data Processing**: Standardizes and cleans the raw energy and weather data.
- **Feature Engineering**: Cultivates predictors that will fuel our machine learning models.
- **Model Training**: Constructs separate pipelines for XGboost and Random Forest, each responsible for its own predictive prowess.
- **Model Evaluation**: A dedicated pipeline assesses performance, crystallizing predictions against reality.

### Kedro Visualization

The Kedro Viz tool provides an interactive canvas to visualize and understand the pipeline structure. It illustrates data flow, dependencies, and the orchestration of nodes and pipelines.


## 📁 Project Structure

A peek into the Kedro project's layout:

```
Kedro-Energy-Forecasting/
│
├── conf/                                    # Configuration files for Kedro project
├── data/
│   ├── 01_raw/                              # Raw, unprocessed datasets
│   ├── 02_processed/                        # Cleaned and processed data ready for analysis
│   ├── 03_training_data/                    # Datasets used for model training
│   ├── 04_reporting/                        # Data for reporting and visualization
│   └── 05_model_output/                     # Outputs from the trained models
│
├── notebooks/                               # Jupyter notebooks for exploratory analysis and prototyping
├── src/
│   ├── pipelines/                           # Sub-directories for each pipeline within the project
│   └── nodes/                               # Individual tasks (nodes) within each pipeline
├── logs/                                    # Generated logs from running Kedro pipelines
├── README.md                                # Project documentation and setup guide
└── requirements.txt                         # Project dependencies
```




## 🚀 Getting Started

Embark on a journey from data to prediction:

1. **Clone the Repository**: Secure a local copy of the code.
2. **Environment Setup**: Opt for a virtual environment using Conda or venv.
3. **Install Dependencies**: Execute `pip install -r requirements.txt` within your chosen environment.
4. **Run the Kedro Pipeline**: Invoke `kedro run` to set the wheels of prediction in motion.

_Need guidance on commands? Peek into the Makefile or use `kedro --help` for assistance._

## 🌐 Let's Connect!

You can connect with me on **LinkedIn** or check out my **GitHub repositories**:

<div align="center">
  <a href="https://www.linkedin.com/in/labrijisaad/">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/labrijisaad">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</div>
