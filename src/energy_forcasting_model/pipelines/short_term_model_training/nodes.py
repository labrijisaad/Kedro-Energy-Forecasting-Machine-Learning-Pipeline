import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xgboost as xgb


def create_features(df: pd.DataFrame, feature_params: dict):
    """
    Create time series features based on time series index and add lag and rolling features for specified columns.
    Adapted to accept feature parameters as a single dictionary and addresses DataFrame fragmentation issues.
    """
    column_names = feature_params["column_names"]
    lags = feature_params["lags"]
    window_sizes = feature_params["window_sizes"]

    # List to store created feature names
    created_features = []

    # Basic time series features
    basic_features = ["dayofweek", "quarter", "month", "year", "dayofyear"]
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
                df[column_name].shift(1).rolling(window=window).mean().rename(rolling_mean_name)
            )

    # Concatenate lag features and rolling window features
    df = pd.concat([df] + lag_features + rolling_mean_features, axis=1)
    created_features.extend([f.name for f in lag_features + rolling_mean_features])

    return df, created_features


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

    # Splitting the data into train and test sets based on the defined Threshold
    train_df = featured_data.loc[featured_data.index < threshold].copy()
    test_df = featured_data.loc[featured_data.index >= threshold].copy()

    # Define the X_train / y_train and X_test / y_test
    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    return X_train, y_train, X_test, y_test


def train_test_split_plot(y_train, y_test, params):
    """
    Generates a plot visualizing the train/test split of data over time.
    """
    threshold = pd.to_datetime(params["threshold"])

    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(12, 7))

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
