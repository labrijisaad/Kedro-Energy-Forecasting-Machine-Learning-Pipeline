from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_features, prepare_train_test_sets, train_test_split_plot


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
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
                tags=["feature_creation", "short_term_model_training"],
            ),
            node(
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
                tags=["data_splitting", "short_term_model_training"],
            ),
            node(
                func=train_test_split_plot,
                inputs=[
                    "y_train_short_term_model",
                    "y_test_short_term_model",
                    "params:feature_splitting_short_term_model",
                ],
                outputs="train_test_split_visualization",
                name="train_test_split_plot_node",
                tags=["train_test_split_plot", "short_term_model_training"],
            ),
        ],
        tags="short_term_model_training",
        namespace="short_term_model_training",
        inputs="processed_weather_and_consumption_data",
        outputs=[
            "X_train_short_term_model",
            "y_train_short_term_model",
            "X_test_short_term_model",
            "y_test_short_term_model",
            "train_test_split_visualization",
        ],
    )
