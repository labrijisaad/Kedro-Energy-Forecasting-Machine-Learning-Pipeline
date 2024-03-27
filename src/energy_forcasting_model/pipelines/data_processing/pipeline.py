from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (prepare_power_consumption_data, 
                    prepare_weather_data, 
                    preprocess_weather_data,
                    merge_consumption_and_weather_data)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=prepare_power_consumption_data,
                inputs="household_power_consumption",
                outputs="power_consumption_data",
                name="prepare_power_consumption_data_node",
            ),
            node(
                func=prepare_weather_data,
                inputs=["weather_data_part1", "weather_data_part2"],
                outputs="weather_data",
                name="prepare_weather_data_node",
            ),
            node(
                func=preprocess_weather_data,
                inputs=["weather_data", "params:data_processing"],
                outputs="processed_weather_data",
                name="preprocess_weather_data_node",
            ),
            node(
                func=merge_consumption_and_weather_data,
                inputs=["power_consumption_data", "processed_weather_data"],
                outputs="weather_and_consumption_data",
                name="merge_consumption_and_weather_data_node",
            ),
        ]
    )
