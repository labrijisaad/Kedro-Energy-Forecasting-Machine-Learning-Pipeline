# `Kedro` Machine Learning Pipeline 🏯

<p align="center">
  <img src="https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/b63b891c-acf0-423e-8ca0-d8baa74a51e6" width="70%" />
</p>

<blockquote align="center">
  <i>"This DALL-E generated image, within Japan, Kedro orchestrates the rhythm of renewable insights amidst the choreography of data and predictions."</i>
</blockquote>

## 📘 Introduction

In this project, I challenged myself to **transform notebook-based code for model training into a Kedro pipeline**. The goal is to create modular, easy-to-train pipelines that follow the **best MLOps practices**, simplifying the deployment of ML models. With Kedro, you can execute just one command to train your models and obtain your pickle files, performance figures, etc. (Yes, just **ONE** command✌️). Parameters can be easily adjusted in a YAML file, allowing for the addition of different steps and the testing of various models with ease. Additionally, Kedro provides **visualization** and **logging features** to keep you informed about everything. **You can create all types of pipelines, not only for machine learning but for any data-driven workflow.**

For an in-depth understanding of **Kedro**, consider exploring the official documentation at [Kedro's Documentation](https://docs.kedro.org/en/stable/introduction/index.html).

## 🎯 Project Goals

The objectives were:
- Make the code in a Notebook **production-ready** and **easily deployable**.
- Allow **easy** addition of models and their performance graphs in the pipeline.
- Adopt the Kedro framework to produce **reproducible**, **modular**, and **scalable workflows**.

## 🛠️ Preparation & Prototyping in Notebooks

Before I started making Kedro pipelines, I tried out my ideas in Jupyter notebooks. Check the `notebooks` folder to see how I did it:

- **[EDA & Data Preparation - Energy_Forecasting.ipynb](./notebooks/EDA%20&%20Data%20Preparation%20-%20Energy_Forecasting.ipynb)**: Offers insights into how I analyzed the data and prepared it for modeling, including data preparation and cleaning processes.
  
- **[Machine Learning - Energy_Forecasting.ipynb](./notebooks/Machine%20Learning%20-%20Energy_Forecasting.ipynb)**: Documents how I evaluated and trained various Machine Learning models, testing the **Random Forest**, **XGBoost**, and **LightGBM** models.


## 🧩 Project Workflow

Within the `src` directory lies the essence, with each component neatly arranged in a Kedro pipeline:

- **Data Processing**: Standardizes and cleans data in ZIP and CSV formats, preparing it for analysis. 🔍
- **Feature Engineering**: Creates new features. 🛠️
- **Train-Test Split Pipeline**: A dedicated pipeline to split the data into training and test sets. 📊
- **Model Training + Model Evaluation**: Constructs separate pipelines for **XGBoost**, **LightGBM** and **Random Forest**, modular and independent, capable of training in async mode. 🤖

### Kedro Visualization

The `Kedro Viz tool` provides an interactive canvas to visualize and **understand the pipeline structure**. It illustrates data flow, dependencies, and the orchestration of nodes and pipelines. Here is the visualization of this project: 
![kedro-pipeline](https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/43354fe6-45eb-4bb0-8f9c-f64f1c6bbeea)

With this tool, the understanding of data progression, outputs, and interactivity is greatly simplified. Kedro Viz allows users to inspect samples of data, view parameters, analyze figures, and much more, enriching the user experience with enhanced transparency and interactivity.

## 📜 Logging and Monitoring

Logging is integral to understanding and troubleshooting pipelines. This project leverages Kedro's logging capabilities to provide real-time insights into pipeline execution, highlighting progress, warnings, and errors. This GIF demonstrates the use of the `kedro run` or `make run` command, showcasing the logging output in action:

<p align="center">
  <img src="https://github.com/labrijisaad/Kedro-Energy-Forecasting-Machine-Learning-Pipeline/assets/74627083/beccb89d-82bd-4233-94bf-cab92e36b5eb" width="70%" />
</p>

Notice how the nodes are executed sequentially, and observe the **RMSE outputs during validation** for the **XGBoost model**. Logging in Kedro is highly customizable, allowing for tailored monitoring that meets the user's specific needs.

## 📁 Project Structure

A _simplified_ overview of the Kedro project's structure:

```
Kedro-Energy-Forecasting/
│
├── conf/                                                # Configuration files for Kedro project
│   ├── base/                                             
│   │   ├── catalog.yml                                  # Data catalog with dataset definitions
│   │   ├── parameters_data_processing_pipeline.yml      # Parameters for data processing
│   │   ├── parameters_feature_engineering_pipeline.yml  # Parameters for feature engineering
│   │   ├── parameters_random_forest_pipeline.yml        # Parameters for Random Forest pipeline
│   │   ├── parameters_lightgbm_training_pipeline.yml    # Parameters for LightGBM pipeline
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
│   │   ├── lightgbm_training_pipeline/                  # LightGBM pipeline
│   │   ├── train_test_split_pipeline/                   # Train-test split pipeline
│   │   └── xgboost_training_pipeline/                   # XGBoost training pipeline
│   └── energy_forecasting_model/                        # Main module for the forecasting model
│
├── .gitignore                                           # Untracked files to ignore
├── Makefile                                             # Set of tasks to be executed
├── README.md                                            # Project documentation and setup guide
└── requirements.txt                                     # Project dependencies
```

## 🚀 Getting Started

Turn **raw CSV data** into a **trained pickle Machine Learning model** with these steps:

1. **Clone the Repository**: Download a copy of the code to your computer.
2. **Set Up the Environment**: Create a virtual environment using Conda or venv.
3. **Install Dependencies**: Run `pip install -r requirements.txt` in your environment to install the required libraries.
4. **Run the Kedro Pipeline**: `make run` or `kedro run` – and witness magic 🪄
5. **Review the Results**: After running the pipeline, look in the `04_reporting` and `05_model_output` directories to see your model's performance and results.
6. **(Optional) Launch Kedro Viz**: To see a visual representation of your pipeline, run `make viz` or `kedro run viz`.

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