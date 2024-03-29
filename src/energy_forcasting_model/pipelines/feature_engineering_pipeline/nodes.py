import pandas as pd


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
