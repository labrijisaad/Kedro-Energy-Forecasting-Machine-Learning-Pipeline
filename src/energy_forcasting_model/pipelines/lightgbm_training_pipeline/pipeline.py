from kedro.pipeline import Pipeline, node, pipeline

from kedro.pipeline import Pipeline, pipeline

from .nodes import train_lightgbm_model

from ..random_forest_pipeline.nodes import (
    plot_real_data_and_predictions_with_train,
    plot_feature_importance,
    generate_predictions,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(  # Node 1: Train LightGBM Model
                func=train_lightgbm_model,
                inputs=["X_train", "y_train", "params:lightgbm_model_params"],
                outputs="lightgbm_model",
                name="train_lightgbm_model_node",
                tags=["model_training", "lightgbm"],
            ),
            node(  # Node 2: Plot Feature Importance
                func=plot_feature_importance,
                inputs=["lightgbm_model", "X_train"],
                outputs="lightgbm_feature_importance_plot",
                name="plot_feature_importance_node",
                tags=[
                    "feature_importance",
                    "visualization",
                    "lightgbm",
                    "model_training",
                ],
            ),
            node(  # Node 3: Generate Predictions
                func=generate_predictions,
                inputs=["X_test", "lightgbm_model"],
                outputs="lightgbm_model_predictions",
                name="generate_predictions_node",
                tags=["predictions", "lightgbm", "model_training"],
            ),
            node(  # Node 4: Plot Real Data and Predictions
                func=plot_real_data_and_predictions_with_train,
                inputs=["y_train", "y_test", "lightgbm_model_predictions"],
                outputs="real_data_and_lightgbm_predictions_plot",
                name="plot_real_data_and_predictions_node",
                tags=["data_visualization", "lightgbm", "model_training"],
            ),
        ],
        tags="model_training",
        namespace="lightgbm_training_pipeline",
        inputs=[
                        "X_train",
                        "y_train",
                        "X_test",
                        "y_test",
        ],
        outputs=[
"lightgbm_model",
"lightgbm_feature_importance_plot",
"real_data_and_lightgbm_predictions_plot",
        ],
    )
