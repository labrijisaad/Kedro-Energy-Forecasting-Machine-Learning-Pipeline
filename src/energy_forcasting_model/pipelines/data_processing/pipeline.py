from kedro.pipeline import Pipeline, node, pipeline

from .nodes import prepare_power_consumption_data, prepare_weather_data, preprocess_weather_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=prepare_power_consumption_data,
                inputs="household_power_consumption",
                outputs="preprocessed_power_consumption_df",
                name="prepare_power_consumption_data_node",
            ),
            node(
                func=prepare_weather_data,
                inputs=["weather_data_part1", "weather_data_part2"],
                outputs="weather_df",
                name="prepare_weather_data_node",
            ),
            node(
                func=preprocess_weather_data,
                inputs=["weather_df", "params:data_processing"],
                outputs="processed_weather_df",
                name="preprocess_weather_data_node",
            ),
        ]
    )
