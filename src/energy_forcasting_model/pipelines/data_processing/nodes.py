import pandas as pd

def import_data_1(file):
    return file


def import_data_2(file):
    return file


def import_data_3(file):
    return file


def transform_data(file1, file2, file3):
    transformed_file = ""
    return transformed_file




def prepare_power_consumption_data(consumptions: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the household power consumption data.

    Args:
        consumptions (pd.DataFrame): DataFrame containing the power consumption data.

    Returns:
        pd.DataFrame: The preprocessed power consumption data, resampled daily.
    """

    # Standardise column names using lower case
    consumptions.rename(
        columns={
            'Date': 'date',
            'Time': 'time',
            'Global_active_power': 'total_consumption'
        },
        inplace=True
    )

    # Define the dataframe index based on the timestamp (date-time)
    consumptions.index = pd.to_datetime(
        consumptions.date + "-" + consumptions.time,
        format="%d/%m/%Y-%H:%M:%S"
    )

    # Drop the date and time variables that are now redundant with the index
    consumptions.drop(columns=['date', 'time'], inplace=True)

    # Resample the data to daily sums
    consumptions_df = consumptions.resample('D').sum()

    return consumptions_df