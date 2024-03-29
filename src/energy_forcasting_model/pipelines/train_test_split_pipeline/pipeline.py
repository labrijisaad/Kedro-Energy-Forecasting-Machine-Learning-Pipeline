from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    create_features,
    prepare_train_test_sets,
    train_test_split_plot
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node( # Node 1
                func=create_features,
                inputs=[
                    "processed_weather_and_consumption_data",
                    "params:feature_engineering_short_term_model",
                ],
                outputs=[
                    "featured_data_short_term_model",
                    "created_features_short_term_model",
                ],
                name="create_features_node",
                tags=["feature_creation"],
            ),
            node( # Node 2
                func=prepare_train_test_sets,
                inputs=[
                    "featured_data_short_term_model",
                    "created_features_short_term_model",
                    "params:feature_splitting_short_term_model",
                ],
                outputs=[
                    "X_train_short_term_model",
                    "y_train_short_term_model",
                    "X_test_short_term_model",
                    "y_test_short_term_model",
                ],
                name="train_test_split_node",
                tags=["data_splitting"],
            ),
            node( # Node 3
                func=train_test_split_plot,
                inputs=[
                    "y_train_short_term_model",
                    "y_test_short_term_model",
                    "params:feature_splitting_short_term_model",
                ],
                outputs="train_test_split_visualization",
                name="train_test_split_plot_node",
                tags=["train_test_split_plot"],
            ),
        ],
        tags="train_test_split_pipeline",
        namespace="short_term_train_test_split_pipeline",
        inputs="processed_weather_and_consumption_data",
        outputs=[
            "train_test_split_visualization",
            "X_train_short_term_model",
            "y_train_short_term_model",
            "X_test_short_term_model",
            "y_test_short_term_model",
        ],
    )