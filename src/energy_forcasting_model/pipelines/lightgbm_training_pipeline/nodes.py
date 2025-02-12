import lightgbm as lgb
import logging

def train_lightgbm_model(X_train, y_train, params):
    """
    Trains a LightGBM regression model using the given training data and parameters.
    """
    # Initialize logger
    logger = logging.getLogger(__name__)

    # Extract model parameters and data types
    model_params = {k: v for k, v in params.items() if k != "data_types"}
    data_types = params.get("data_types", {})

    # Convert specified columns to boolean based on provided data types
    boolean_columns = data_types.get("boolean_columns", [])
    for col in boolean_columns:
        if col in X_train.columns:
            logger.debug(f"Converting column {col} to boolean.")
            X_train[col] = X_train[col].astype("bool")

    # Log the start and parameters of the training process
    logger.info("Starting LightGBM model training...")
    logger.info(f"LightGBM parameters: {model_params}")

    # Drop rows with null values from X_train and align y_train
    X_train_clean = X_train.dropna()
    y_train_clean = y_train.loc[X_train_clean.index]

    # Log how many rows were dropped
    dropped_rows = X_train.shape[0] - X_train_clean.shape[0]
    logger.info(f"Dropped {dropped_rows} rows with null values from training data.")

    # Create an instance of LGBMRegressor with parameters unpacked
    lgbm_model = lgb.LGBMRegressor(**model_params)

    # Training the model
    logger.info("Training the LightGBM model...")
    lgbm_model.fit(
        X_train_clean,
        y_train_clean,
        eval_set=[(X_train_clean, y_train_clean)],
        eval_metric=model_params.get("metric", "l2"),
    )

    # Log the completion of the training process
    logger.info("LightGBM model training completed successfully.")

    return lgbm_model
