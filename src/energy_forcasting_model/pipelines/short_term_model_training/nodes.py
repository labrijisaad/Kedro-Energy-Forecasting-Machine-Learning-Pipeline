import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xgboost as xgb
import seaborn as sns


# Node 1
def create_features(df: pd.DataFrame, feature_params: dict):
    """
    Create time series features based on time series index and add lag and rolling features for specified columns.
    Adapted to accept feature parameters as a single dictionary and addresses DataFrame fragmentation issues.
    """
    column_names = feature_params["column_names"]
    lags = feature_params["lags"]
    window_sizes = feature_params["window_sizes"]
    basic_features = feature_params["basic_features"]

    # List to store created feature names
    created_features = []

    for feature in basic_features:
        # Add basic time series features to the DataFrame
        df[feature] = getattr(df.index, feature)
        created_features.append(feature)

    # Create lag features and rolling window features using pd.concat
    lag_features = []
    rolling_mean_features = []
    for column_name in column_names:
        # Lag features for each specified column
        for lag in lags:
            lag_feature_name = f"{column_name}_lag_{lag}"
            lag_features.append(df[column_name].shift(lag).rename(lag_feature_name))

        # Rolling window features for each specified column
        for window in window_sizes:
            rolling_mean_name = f"{column_name}_rolling_mean_{window}"
            rolling_mean_features.append(
                df[column_name]
                .shift(1)  # Shift by one day
                .rolling(window=window)
                .mean()
                .rename(rolling_mean_name)
            )

    # Concatenate lag features and rolling window features
    df = pd.concat([df] + lag_features + rolling_mean_features, axis=1)
    created_features.extend([f.name for f in lag_features + rolling_mean_features])

    return df, created_features


# Node 2
def prepare_train_test_sets(featured_data, created_features_list, params):
    """
    Splits the featured data into training and testing datasets based on a specified date threshold.
    """
    TARGET = params["target"]
    threshold = pd.to_datetime(params["threshold"])

    # # Ensure the DataFrame index is in datetime format
    featured_data.index = pd.to_datetime(featured_data.index)

    # Combine created features and external features for model input
    FEATURES = created_features_list

    # Splitting the data into train and test sets based on the Threshold
    train_df = featured_data.loc[featured_data.index < threshold]
    test_df = featured_data.loc[featured_data.index >= threshold]

    # Define the X_train / y_train and X_test / y_test
    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    return X_train, y_train, X_test, y_test


# Node 3
def train_test_split_plot(y_train, y_test, params):
    """
    Generates a plot visualizing the train/test split of data over time.
    """
    threshold = pd.to_datetime(params["threshold"])

    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(20, 10))

    # Enhancing the plot aesthetics
    ax.plot(
        y_train.index, y_train, label="Training Set", color="dodgerblue", linewidth=2
    )
    ax.plot(y_test.index, y_test, label="Test Set", color="coral", linewidth=2)
    ax.axvline(
        x=threshold,
        color="dimgray",
        linestyle="--",
        linewidth=2,
        label="Train/Test Split Date",
    )

    # Formatting the date axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)

    # Setting titles and labels with an enhanced appearance
    ax.set_title(
        "Train/Test Split - Data Visualization", fontsize=16, fontweight="bold"
    )
    ax.set_xlabel("Date", fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Consumption", fontsize=14, fontweight="bold")

    # Adding a grid and legend for better readability
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend(frameon=True, framealpha=0.9, shadow=True, borderpad=1)

    # Adjusting the layout
    plt.tight_layout()

    plt.close(fig)
    return fig


# Node 4
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


# Node 5
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


# Node 6
def generate_predictions(X_test, trained_model):
    """
    Generates predictions for the test data using the trained XGBoost model.
    """
    predictions = trained_model.predict(X_test)
    return predictions


# Node 7
def plot_real_data_and_predictions_with_train(y_train, y_test, predictions, params):
    """
    Generates a plot comparing the actual consumption data with model predictions
    and includes training data.
    """

    # Converting y_test and y_train to DataFrame for ease of plotting
    y_test_df = pd.DataFrame(y_test, columns=["total_consumption"])
    y_train_df = pd.DataFrame(y_train, columns=["total_consumption"])

    # Adding predictions to the test DataFrame
    y_test_df["Model_Prediction"] = predictions

    # Ensure the index is in datetime format for plotting
    y_test_df.index = pd.to_datetime(y_test_df.index)
    y_train_df.index = pd.to_datetime(y_train_df.index)

    # Extracting threshold for plotting
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

    # Adding a vertical line for the threshold
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
