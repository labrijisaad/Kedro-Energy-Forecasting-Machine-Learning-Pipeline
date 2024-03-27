import pandas as pd
import re

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

def clean_string(s):
    """
    Cleans a string: replaces spaces with underscores, removes special characters, and converts to lowercase.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', s.replace(' ', '_')).lower()

def calculate_day_length(df, sunrise_col='sunrise', sunset_col='sunset'):
    """
    Adds 'day_length' to df calculated from 'sunrise' and 'sunset', and drops these columns.
    Assumes sunrise and sunset are in the format 'HH:MM:SS'.
    """
    # Convert sunrise and sunset to datetime, assuming they are strings in 'HH:MM:SS' format
    sunrise = pd.to_datetime(df[sunrise_col], format='%H:%M:%S')
    sunset = pd.to_datetime(df[sunset_col], format='%H:%M:%S')

    # Calculate day length in hours
    df['day_length'] = (sunset - sunrise).dt.total_seconds() / 3600.0
    
    return df.drop([sunrise_col, sunset_col], axis=1)

def preprocess_weather_data(df, params):
    """
    Preprocesses weather data: sorts by index, filters by date, selects columns, encodes a column, and calculates day length.
    """
    # Extract parameters
    start_date = params['date_interval']['start_date']
    end_date = params['date_interval']['end_date']
    columns_to_keep = params['columns_to_keep']
    column_to_encode = params['column_to_encode']

    # Ensure the DataFrame is sorted by its index
    df.sort_index(inplace=True)
    
    # Select specified columns
    df_selected = df.loc[:, columns_to_keep].copy()
    
    # Filter by date range
    df_filtered = df_selected.loc[(df_selected.index >= start_date) & (df_selected.index <= end_date)].copy()
    
    # Clean and encode specified column
    df_filtered[column_to_encode] = df_filtered[column_to_encode].apply(clean_string)
    dummies = pd.get_dummies(df_filtered[column_to_encode], prefix=column_to_encode)
    df_encoded = pd.concat([df_filtered, dummies], axis=1).drop(column_to_encode, axis=1)
    
    # Calculate day length and drop original sunrise and sunset columns
    return calculate_day_length(df_encoded)

def merge_consumption_and_weather_data(power_consumption_data: pd.DataFrame, 
               processed_weather_data: pd.DataFrame) -> pd.DataFrame:
    """
    Merges power consumption data with processed weather data on their indices.

    Args:
        power_consumption_data (pd.DataFrame): DataFrame containing power consumption data.
        processed_weather_data (pd.DataFrame): DataFrame containing processed weather data.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    merged_df = pd.merge(power_consumption_data, processed_weather_data, left_index=True, right_index=True)
    return merged_df

def mark_holidays(df: pd.DataFrame, holidays: pd.DataFrame) -> pd.DataFrame:
    """
    Adds an 'is_holiday' column to the DataFrame, indicating whether each date is a holiday.

    Args:
        df (pd.DataFrame): The DataFrame to be augmented with the 'is_holiday' column.
        holidays (pd.DataFrame): DataFrame containing holiday dates.

    Returns:
        pd.DataFrame: The augmented DataFrame with an 'is_holiday' column.
    """
    # Convert the list of dates to a set for faster lookup
    holidays_set = set(holidays['date'].dt.date)

    # Convert the DataFrame index to a Series of dates for the isin() comparison
    index_as_series = pd.Series(df.index.date)

    # Add a new column 'is_holiday' to the DataFrame
    df['is_holiday'] = index_as_series.isin(holidays_set)
    return df