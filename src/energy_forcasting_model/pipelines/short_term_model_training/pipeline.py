from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_features

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_features,
                inputs=["processed_weather_and_consumption_data", "params:feature_engineering"],
                outputs=["featured_data", "created_features_short_term_model"],
                name="create_features_node",
            ),
        ],
        tags="short_term_model_training",
        namespace="short_term_model_training",
        inputs="processed_weather_and_consumption_data",
        outputs=["featured_data", "created_features_short_term_model"]
    )
