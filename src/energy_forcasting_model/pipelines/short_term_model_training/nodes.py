import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def create_features(df: pd.DataFrame, feature_params: dict):
    """
    Create time series features based on time series index and add lag and rolling features for specified columns.
    Adapted to accept feature parameters as a single dictionary and addresses DataFrame fragmentation issues.
    """
    column_names = feature_params["column_names"]
    lags = feature_params["lags"]
    window_sizes = feature_params["window_sizes"]

    # Ensure the DataFrame index is datetime if it's not already
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    feature_frames = [df.copy()]  # Start with a copy of the original DataFrame

    # Generate basic time features
    basic_features = {
        "dayofweek": df.index.dayofweek,
        "quarter": df.index.quarter,
        "month": df.index.month,
        "year": df.index.year,
        "dayofyear": df.index.dayofyear,
    }

    for feature_name, feature_series in basic_features.items():
        feature_frames.append(pd.DataFrame({feature_name: feature_series}))

    # Generate lag and rolling features
    for column_name in column_names:
        for lag in lags:
            lag_feature_name = f"{column_name}_lag_{lag}"
            feature_frames.append(
                pd.DataFrame({lag_feature_name: df[column_name].shift(lag)})
            )

        for window in window_sizes:
            rolling_mean_name = f"{column_name}_rolling_mean_{window}"
            feature_frames.append(
                pd.DataFrame(
                    {rolling_mean_name: df[column_name].shift(1).rolling(window).mean()}
                )
            )

    # Concatenate all features
    df_combined = pd.concat(feature_frames, axis=1, sort=False)

    return df_combined, list(df_combined.columns)


def prepare_train_test_sets(featured_data, created_features_list, params):
    """
    Splits the featured data into training and testing datasets based on a specified date threshold.

    Parameters:
    - featured_data (pd.DataFrame): DataFrame containing the featured data with a datetime index.
    - created_features_list (list): List of created feature names to be included in the model input.
    - params (dict): Dictionary containing external feature names, the target variable name, and the split threshold date.
        - params["external_features"]: List of external feature names to be included in the model input.
        - params["target"]: The name of the target variable.
        - params["threshold"]: The date (YYYY-MM-DD) used to split the data into training and testing sets.

    Ensures that the DataFrame index is in datetime format for proper temporal splitting.

    Returns:
    - X_train (pd.DataFrame): Training dataset features.
    - y_train (pd.Series): Training dataset target variable.
    - X_test (pd.DataFrame): Testing dataset features.
    - y_test (pd.Series): Testing dataset target variable.
    """
    EXTERNAL_FEATURES = params["external_features"]
    TARGET = params["target"]
    threshold = pd.to_datetime(params["threshold"])

    # Ensure the DataFrame index is in datetime format
    featured_data.index = pd.to_datetime(featured_data.index)

    # Combine created features and external features for model input
    FEATURES = created_features_list + EXTERNAL_FEATURES

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

    This function plots the training and testing datasets to visualize the split based
    on a threshold date. It highlights the division with a vertical line and uses
    different colors to differentiate between the training and testing sets.

    Parameters:
    - X_train (pd.DataFrame): Features of the training set.
    - y_train (pd.Series): Target variable of the training set.
    - X_test (pd.DataFrame): Features of the testing set.
    - y_test (pd.Series): Target variable of the testing set.
    - params (dict): Contains 'threshold', the date used to split the training and testing data.

    Returns:
    - fig (matplotlib.figure.Figure): The matplotlib figure object containing the plot.
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
