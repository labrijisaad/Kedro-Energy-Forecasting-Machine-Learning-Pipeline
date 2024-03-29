import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xgboost as xgb
import seaborn as sns


# Node 1
def train_xgboost_model(X_train, y_train, params):
    """
    Trains an XGBoost regression model using the given training data and parameters.
    """
    # Convert specified columns to boolean
    data_types = params.get("data_types", {})
    boolean_columns = data_types.get("boolean_columns", [])

    # Applying conversion for boolean columns
    for col in boolean_columns:
        if col in X_train.columns:
            X_train[col] = X_train[col].astype("bool")

    # Instantiate XGBoost Regressor
    xgb_model = xgb.XGBRegressor(
        base_score=params.get("base_score", 0.5),
        booster=params.get("booster", "gbtree"),
        n_estimators=params.get("n_estimators", 1000),
        early_stopping_rounds=params.get("early_stopping_rounds", 50),
        objective=params.get("objective", "reg:linear"),
        max_depth=params.get("max_depth", 3),
        learning_rate=params.get("learning_rate", 0.01),
        enable_categorical=True,
    )

    # Adjusting verbosity based on YAML configuration
    verbose_eval = params.get("verbose_eval", 100)

    # Train the XGBoost Regressor
    xgb_model.fit(X_train, y_train, verbose=verbose_eval, eval_set=[(X_train, y_train)])

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


# Node 4
def plot_real_data_and_predictions_with_train(y_train, y_test, predictions, params):
    """
    Generates a plot comparing the actual consumption data with model predictions
    and includes training data.
    """

    # Target column name
    TARGET = params["target"]
    # Converting y_test and y_train to DataFrame
    y_test_df = pd.DataFrame(y_test, columns=[TARGET])
    y_train_df = pd.DataFrame(y_train, columns=[TARGET])

    # Adding predictions to the test DataFrame
    y_test_df["Model_Prediction"] = predictions

    # Train / Test split threshold
    threshold = pd.to_datetime(params["threshold"])

    # Plotting
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        y_train_df.index,
        y_train_df["total_consumption"],
        label="Training Data",
        color="blue",
        linewidth=2,
    )
    ax.plot(
        y_test_df.index,
        y_test_df["total_consumption"],
        label="Test Data",
        color="forestgreen",
        linewidth=2,
    )
    ax.scatter(
        y_test_df.index,
        y_test_df["Model_Prediction"],
        label="Model Predictions",
        color="red",
        s=10,
    )

    # Adding a vertical line for the threshold for visual separation
    ax.axvline(
        x=threshold, color="black", linestyle="--", linewidth=2, label="Threshold"
    )

    # Setting the major locator and formatter for the x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)

    # Setting titles and labels
    ax.set_title("Training, Test Data and Model Predictions", fontsize=16)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Value", fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.close(fig)

    return fig
