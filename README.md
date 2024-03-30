# `Kedro` Machine Learning Pipeline 🏯

<p align="center">
  <img src="https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/b63b891c-acf0-423e-8ca0-d8baa74a51e6" width="70%" />
</p>

<blockquote align="center">
  <i>"This DALL-E generated image, within Japan, Kedro orchestrates the rhythm of renewable insights amidst the choreography of data and predictions."</i>
</blockquote>

## 📘 Introduction

In this project, I challenged myself to **transform notebook-based code for model training into a Kedro pipeline**. The idea is to create modular, simple-to-train pipelines following the `best MLOps practices`, to simplify the deployment of ML models. With Kedro, you can execute just one command to train your models and obtain your pickle, performance figures, etc. You can easily adjust parameters in a YAML file, add different steps, and test various models with ease. Additionally, Kedro provides visualization and logging features to keep you informed about everything. 

## 🎯 Project Goals

The objectives were:
- Make the code production-ready and deployable.
- Allow easy addition of models and their performance graphs in the pipeline.
- Adopt the Kedro framework to produce reproducible, modular, and scalable workflows.

## 🧩 Project Workflow

Within the `src` directory lies the essence, with each component neatly arranged in a Kedro pipeline:

- **Data Processing**: Standardizes and cleans data in ZIP and CSV formats, preparing it for analysis. 🔍
- **Feature Engineering**: Creates new features. 🛠️
- **Train-Test Split Pipeline**: A dedicated pipeline to split the data into training and test sets. 📊
- **Model Training + Model Evaluation**: Constructs separate pipelines for XGBoost and Random Forest, modular and independent, capable of training in async mode. 🤖

### Kedro Visualization

The `Kedro Viz tool` provides an interactive canvas to visualize and **understand the pipeline structure**. It illustrates data flow, dependencies, and the orchestration of nodes and pipelines. Here is the visualization of this project: 
![kedro-pipeline](https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/43354fe6-45eb-4bb0-8f9c-f64f1c6bbeea)

With this tool, the understanding of data progression, outputs, and interactivity is greatly simplified. Kedro Viz allows users to inspect samples of data, view parameters, analyze figures, and much more, enriching the user experience with enhanced transparency and interactivity.

## 📜 Logging and Monitoring

Logging is integral to understanding and troubleshooting pipelines. This project leverages Kedro's logging capabilities to provide real-time insights into pipeline execution, highlighting progress, warnings, and errors. This GIF demonstrates the use of the `kedro run` or `make run` command, showcasing the logging output in action:

<p align="center">
  <img src="https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/beccb89d-82bd-4233-94bf-cab92e36b5eb" width="70%" />
</p>

Notice how the nodes are executed sequentially, and observe the RMSE outputs for the XGBoost model. Logging in Kedro is highly customizable, allowing for tailored monitoring that meets the user's specific needs.

## 📁 Project Structure

A simplified overview of the Kedro project's structure:

```
Kedro-Energy-Forecasting/
│
├── conf/                                                # Configuration files for Kedro project
│   ├── base/                                             
│   │   ├── catalog.yml                                  # Data catalog with dataset definitions
│   │   ├── parameters_data_processing_pipeline.yml      # Parameters for data processing
│   │   ├── parameters_feature_engineering_pipeline.yml  # Parameters for feature engineering
│   │   ├── parameters_random_forest_pipeline.yml        # Parameters for Random Forest pipeline
│   │   ├── parameters_train_test_split_pipeline.yml     # Parameters for train-test split
│   │   └── parameters_xgboost_training_pipeline.yml     # Parameters for XGBoost training
│   └── local/                                            
│
├── data/
│   ├── 01_raw/                                          # Raw, unprocessed datasets
│   ├── 02_processed/                                    # Cleaned and processed data ready for analysis
│   ├── 03_training_data/                                # Train/Test Datasets used for model training
│   ├── 04_reporting/                                    # Figures and Results after running the pipelines
│   └── 05_model_output/                                 # Trained pickle models
│
├── src/
│   ├── pipelines/                            
│   │   ├── data_processing_pipeline/                    # Data processing pipeline
│   │   ├── feature_engineering_pipeline/                # Feature engineering pipeline
│   │   ├── random_forest_pipeline/                      # Random Forest pipeline
│   │   ├── train_test_split_pipeline/                   # Train-test split pipeline
│   │   └── xgboost_training_pipeline/                   # XGBoost training pipeline
│   └── energy_forecasting_model/                        # Main module for the forecasting model
│
├── .gitignore                                           # Untracked files to ignore
├── Makefile                                             # Set of tasks to be executed
├── pyproject.toml                                        
├── README.md                                            # Project documentation and setup guide
└── requirements.txt                                     # Project dependencies
```

## 🚀 Getting Started

Transform **raw data** into **Machine Learning Model** with these steps:

1. **Clone the Repository**: Grab your local copy.
2. **Environment Setup**: Opt for a virtual environment using Conda or venv.
3. **Install Dependencies**: Execute `pip install -r requirements.txt` within your chosen environment.
4. **Run the Kedro Pipeline**: `kedro run` – and witness magic.

_Need guidance on commands? Peek into the **Makefile** or use `kedro --help` for assistance._

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
