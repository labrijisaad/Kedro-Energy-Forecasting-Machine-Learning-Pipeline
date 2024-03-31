import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
import logging


from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


def train_random_forest_model(X_train, y_train, params):
    """
    Trains a Random Forest regression model using the given training data and parameters.
    """
    # Initialize logger
    logger = logging.getLogger(__name__)

    # Log the start of the training process
    logger.info("Starting Random Forest model training...")

    # Log model parameters for reproducibility/debugging
    logger.info(
        f"Random Forest parameters: n_estimators={params.get('n_estimators', 600)}, max_depth={params.get('max_depth', 3)}, random_state={params.get('random_state', 42)}"
    )

    rfr_model = RandomForestRegressor(
        n_estimators=params.get("n_estimators", 600),
        max_depth=params.get("max_depth", 3),
        random_state=params.get("random_state", 42),
    )

    # Fit the model
    rfr_model.fit(X_train, y_train.squeeze())

    # Log the completion of the training process
    logger.info("Random Forest model training completed successfully.")

    return rfr_model


# Node 2
def plot_feature_importance(trained_model, X_train):
    """
    Generates a plot of the top 10 features based on importance from a trained XGBoost model.
    """
    # Extracting feature importances
    feature_data_xgb = pd.DataFrame(
        {
            "Feature": X_train.columns,
            "Importance": trained_model.feature_importances_,
            "Model": "XGBoost",
        }
    )

    # Sort by importance and select top 10 features
    top_features_xgb = feature_data_xgb.sort_values(
        by="Importance", ascending=False
    ).head(10)

    # Plotting
    fig, ax = plt.subplots(figsize=(20, 10))

    # XGBoost
    sns.barplot(data=top_features_xgb, x="Importance", y="Feature", ax=ax)
    ax.set_title("XGBoost: Top 10 Features", fontsize=16)
    ax.set_xlabel("Feature Importance", fontsize=12)
    ax.set_ylabel("Feature", fontsize=12)

    plt.tight_layout()
    plt.close(fig)

    return fig


# Node 2
def generate_predictions(X_test, trained_model):
    """
    Generates predictions for the test data using the trained XGBoost model.
    """
    predictions = trained_model.predict(X_test)
    return predictions


def plot_real_data_and_predictions_with_train(y_train, y_test, predictions):
    """
    Generates a plot comparing the actual data with model predictions and includes training data,
    and displays the RMSE score.
    """
    # Initialize logger
    logger = logging.getLogger(__name__)

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    logger.info(f"RMSE for the test set: {rmse:.2f}")

    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(18, 7))

    # Plot training data
    ax.plot(y_train.index, y_train, label="Training Data", color="blue", linewidth=2)

    # Plot test data
    ax.plot(y_test.index, y_test, label="Test Data", color="forestgreen", linewidth=2)

    # Plot predictions
    ax.scatter(y_test.index, predictions, label="Model Predictions", color="red", s=10)

    # Find the last date of the training set to add a vertical line for visual separation
    last_train_date = y_train.index[-1]
    ax.axvline(
        x=last_train_date,
        color="black",
        linestyle="--",
        linewidth=2,
        label="Train/Test Split",
    )

    # Formatting the date axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)

    # Setting titles and labels with RMSE score
    ax.set_title(
        f"Training, Test Data and Model Predictions - RMSE: {rmse:.2f}", fontsize=16
    )
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Value", fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.close(fig)

    return fig
