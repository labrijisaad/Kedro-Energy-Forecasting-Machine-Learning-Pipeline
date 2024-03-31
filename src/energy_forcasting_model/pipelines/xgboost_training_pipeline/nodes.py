import pandas as pd
import matplotlib.pyplot as plt
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
