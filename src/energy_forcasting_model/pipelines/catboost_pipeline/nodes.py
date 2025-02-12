import logging
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor
from shap import TreeExplainer, summary_plot
from sklearn.inspection import partial_dependence, PartialDependenceDisplay

def train_catboost_model(X_train, y_train, params):
    """
    Trains a CatBoost regression model using the given training data and parameters.
    
    Args:
        X_train (DataFrame): Training features.
        y_train (Series/DataFrame): Training target.
        params (dict): Dictionary containing CatBoost parameters.
    
    Returns:
        CatBoostRegressor: Trained CatBoost model.
    """
    # Initialize logger
    logger = logging.getLogger(__name__)
    logger.info("Starting CatBoost model training...")

    # Log model parameters for reproducibility/debugging
    logger.info(
        f"CatBoost parameters: iterations={params['iterations']}, "
        f"depth={params['depth']}, learning_rate={params['learning_rate']}, "
        f"loss_function={params['loss_function']}, eval_metric={params['eval_metric']}, "
        f"verbose_eval={params.get('verbose_eval', True)}"
    )

    # Convert specified columns to boolean based on provided data types
    boolean_columns = params.get("data_types", {}).get("boolean_columns", [])
    for col in boolean_columns:
        if col in X_train.columns:
            logger.debug(f"Converting column {col} to boolean.")
            X_train[col] = X_train[col].astype("bool")

    # Drop rows with null values from X_train and align y_train
    X_train_clean = X_train.dropna()
    y_train_clean = y_train.loc[X_train_clean.index]

    # Log how many rows were dropped
    dropped_rows = X_train.shape[0] - X_train_clean.shape[0]
    logger.info(f"Dropped {dropped_rows} rows with null values from training data.")

    # Instantiate CatBoostRegressor with the given parameters
    cat_model = CatBoostRegressor(
        allow_writing_files=False,
        iterations=params["iterations"],
        depth=params["depth"],
        learning_rate=params["learning_rate"],
        loss_function=params["loss_function"],
        eval_metric=params["eval_metric"],
        random_seed=params.get("random_state", 42),
        verbose=params.get("verbose_eval", True)
    )

    # Train the model with an evaluation set for monitoring
    logger.info("Training the CatBoost model...")
    cat_model.fit(
        X_train_clean,
        y_train_clean,
        eval_set=[(X_train_clean, y_train_clean)],
        verbose=params.get("verbose_eval", True)
    )

    # Log the completion of the training process
    logger.info("CatBoost model training completed successfully.")

    return cat_model


def explain_catboost_model(model, X_train):
    """
    Generates a SHAP summary plot for the given CatBoost model.

    Args:
        model: Trained CatBoost model.
        X_train: Training feature set.

    Returns:
        A matplotlib figure object with the SHAP summary plot.
    """
    logger = logging.getLogger(__name__)
    logger.info("Computing SHAP values for CatBoost model...")

    # Create a SHAP explainer and compute SHAP values
    explainer = TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)

    # Create a SHAP summary plot
    plt.figure()
    summary_plot(shap_values, X_train, show=False)
    fig = plt.gcf()  # Get current figure
    plt.close(fig)
    
    logger.info("SHAP summary plot created successfully.")
    return fig


def plot_partial_dependence_catboost(model, X_train, features):
    """
    Generates a partial dependence plot for specified features using the trained CatBoost model.
    
    Args:
        model: Trained CatBoost model.
        X_train (DataFrame): Training features.
        features (list): List of feature names or indices for which to compute partial dependence.
    
    Returns:
        matplotlib.figure.Figure: The partial dependence plot figure.
    """
    logger = logging.getLogger(__name__)
    logger.info("Creating partial dependence plot for CatBoost model...")
    
    # Create the plot using scikit-learn's PartialDependenceDisplay
    fig, ax = plt.subplots(figsize=(12, 8))
    display = PartialDependenceDisplay.from_estimator(
        model,
        X_train,
        features=features,
        ax=ax
    )
    ax.set_title("Partial Dependence Plot")
    plt.tight_layout()
    plt.close(fig)
    
    logger.info("Partial dependence plot created successfully.")
    return fig
