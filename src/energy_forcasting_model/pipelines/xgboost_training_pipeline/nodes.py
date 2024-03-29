import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xgboost as xgb
import seaborn as sns
import logging


# Node 1
def train_xgboost_model(X_train, y_train, params):
    """
    Trains an XGBoost regression model using the given training data and parameters.
    """
    # Initialize logger
    logger = logging.getLogger(__name__)

    # Log the start of the training process
    logger.info("Starting XGBoost model training...")

    # Log model parameters for reproducibility/debugging
    logger.info(
        f"XGBoost parameters: base_score={params['base_score']}, booster={params['booster']}, n_estimators={params['n_estimators']}, early_stopping_rounds={params['early_stopping_rounds']}, objective={params['objective']}, max_depth={params['max_depth']}, learning_rate={params['learning_rate']}, enable_categorical=True, verbose_eval={params['verbose_eval']}"
    )

    # Convert specified columns to boolean based on provided data types
    boolean_columns = params["data_types"]["boolean_columns"]
    for col in boolean_columns:
        if col in X_train.columns:
            logger.debug(f"Converting column {col} to boolean.")
            X_train[col] = X_train[col].astype("bool")

    # Instantiate XGBoost Regressor with the given parameters
    xgb_model = xgb.XGBRegressor(
        base_score=params["base_score"],
        booster=params["booster"],
        n_estimators=params["n_estimators"],
        early_stopping_rounds=params["early_stopping_rounds"],
        objective=params["objective"],
        max_depth=params["max_depth"],
        learning_rate=params["learning_rate"],
        enable_categorical=True,
    )

    # Training the model with verbosity based on the provided configuration
    logger.info("Training the XGBoost model...")
    xgb_model.fit(
        X_train, y_train, verbose=params["verbose_eval"], eval_set=[(X_train, y_train)]
    )

    # Log the completion of the training process
    logger.info("XGBoost model training completed successfully.")

    return xgb_model


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
