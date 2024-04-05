from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_features


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                                            func=create_features,
                                            inputs=[
                                                "processed_weather_and_consumption_data",
                                                "params:feature_engineering",
                                            ],
                                            outputs=[
                                                "featured_data",
                                                "created_features",
                                            ],
                                            name="create_features_node",
                                            tags=["feature_creation"],
                                        ),
        ],
        tags="feature_engineering_pipeline",
        namespace="feature_engineering_pipeline",
        inputs=["processed_weather_and_consumption_data"],
        outputs=["featured_data", "created_features"],
    )
