from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_features, prepare_train_test_sets, train_test_split_plot


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(  # Node 1
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
            node(  # Node 2
                func=prepare_train_test_sets,
                inputs=[
                    "featured_data",
                    "created_features",
                    "params:feature_splitting",
                ],
                outputs=[
                    "X_train",
                    "y_train",
                    "X_test",
                    "y_test",
                ],
                name="train_test_split_node",
                tags=["data_splitting"],
            ),
            node(  # Node 3
                func=train_test_split_plot,
                inputs=[
                    "y_train",
                    "y_test",
                    "params:feature_splitting",
                ],
                outputs="train_test_split_visualization",
                name="train_test_split_plot_node",
                tags=["train_test_split_plot"],
            ),
        ],
        tags="train_test_split_pipeline",
        namespace="train_test_split_pipeline",
        inputs="processed_weather_and_consumption_data",
        outputs=[
            "train_test_split_visualization",
            "X_train",
            "y_train",
            "X_test",
            "y_test",
        ],
    )
