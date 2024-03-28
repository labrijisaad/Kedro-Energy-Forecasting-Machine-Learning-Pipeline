import pandas as pd

def create_features(df: pd.DataFrame, feature_params: dict):
    """
    Create time series features based on time series index and add lag and rolling features for specified columns.
    Adapted to accept feature parameters as a single dictionary and addresses DataFrame fragmentation issues.
    """
    column_names = feature_params['column_names']
    lags = feature_params['lags']
    window_sizes = feature_params['window_sizes']

    # Ensure the DataFrame index is datetime if it's not already
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    feature_frames = [df.copy()]  # Start with a copy of the original DataFrame

    # Generate basic time features
    basic_features = {'dayofweek': df.index.dayofweek, 'quarter': df.index.quarter,
                      'month': df.index.month, 'year': df.index.year, 'dayofyear': df.index.dayofyear}

    for feature_name, feature_series in basic_features.items():
        feature_frames.append(pd.DataFrame({feature_name: feature_series}))

    # Generate lag and rolling features
    for column_name in column_names:
        for lag in lags:
            lag_feature_name = f'{column_name}_lag_{lag}'
            feature_frames.append(pd.DataFrame({lag_feature_name: df[column_name].shift(lag)}))

        for window in window_sizes:
            rolling_mean_name = f'{column_name}_rolling_mean_{window}'
            feature_frames.append(pd.DataFrame({rolling_mean_name: df[column_name].shift(1).rolling(window).mean()}))

    # Concatenate all features
    df_combined = pd.concat(feature_frames, axis=1, sort=False)

    return df_combined, list(df_combined.columns)
