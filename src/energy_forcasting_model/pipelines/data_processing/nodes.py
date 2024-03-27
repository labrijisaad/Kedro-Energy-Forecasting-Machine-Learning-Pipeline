import pandas as pd
from typing import Dict

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


def prepare_weather_data(weather_data_part1: pd.DataFrame, 
                         weather_data_part2: pd.DataFrame) -> pd.DataFrame:
    """
    Concatenates two parts of weather data into a single DataFrame.

    Args:
        weather_data_part1 (pd.DataFrame): The first part of the weather data.
        weather_data_part2 (pd.DataFrame): The second part of the weather data.

    Returns:
        pd.DataFrame: The concatenated DataFrame.
    """
    weather_df = pd.concat([weather_data_part1, weather_data_part2])
    return weather_df

