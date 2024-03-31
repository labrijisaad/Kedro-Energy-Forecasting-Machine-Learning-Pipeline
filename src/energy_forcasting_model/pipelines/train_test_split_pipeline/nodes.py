import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


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
def train_test_split_plot(y_train, y_test):
    """
    Generates a plot visualizing the train/test split of data over time, including a vertical
    line to indicate the split point.
    """
    # Create the figure and axes objects
    fig, ax = plt.subplots(figsize=(18, 6))

    # Enhancing the plot aesthetics
    ax.plot(
        y_train.index, y_train, label="Training Set", color="dodgerblue", linewidth=2
    )
    ax.plot(y_test.index, y_test, label="Test Set", color="coral", linewidth=2)

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

    # Find the last date of the training set and add a vertical line
    last_train_date = y_train.index[-1]
    ax.axvline(
        x=last_train_date,
        color="grey",
        linestyle="--",
        linewidth=2,
        label="Train/Test Split",
    )

    # Adjusting the layout
    plt.tight_layout()

    plt.close(fig)
    return fig
