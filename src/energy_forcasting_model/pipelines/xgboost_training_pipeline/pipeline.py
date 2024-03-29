from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    train_xgboost_model,
    plot_feature_importance,
    generate_predictions,
    plot_real_data_and_predictions_with_train,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(  # Node 1
                func=train_xgboost_model,
                inputs=[
                    "X_train",
                    "y_train",
                    "params:xgboost_model_params",
                ],
                outputs="xgboost_model",
                name="train_xgboost_model_node",
                tags=["model_training", "xgboost", "model_training"],
            ),
            node(  # Node 2
                func=plot_feature_importance,
                inputs=[
                    "xgboost_model",
                    "X_train",
                ],
                outputs="xgboost_feature_importance_plot",
                name="plot_feature_importance_node",
                tags=[
                    "feature_importance",
                    "visualization",
                    "xgboost",
                    "model_training",
                ],
            ),
            node(  # Node 3
                func=generate_predictions,
                inputs=[
                    "X_test",
                    "xgboost_model",
                ],
                outputs="xgboost_model_predictions",
                name="generate_predictions_node",
                tags=["predictions", "xgboost", "model_training"],
            ),
            node(  # Node 4
                func=plot_real_data_and_predictions_with_train,
                inputs=[
                    "y_train",
                    "y_test",
                    "xgboost_model_predictions",
                    "params:xgboost_model_params",
                ],
                outputs="real_data_and_xgboost_predictions_plot",
                name="plot_real_data_and_predictions_node",
                tags=["data_visualization", "xgboost", "model_training"],
            ),
        ],
        tags="model_training",
        namespace="xgboost_training_pipeline",
        inputs=[
            "X_train",
            "y_train",
            "X_test",
            "y_test",
        ],
        outputs=[
            "xgboost_model",
            "xgboost_feature_importance_plot",
            "real_data_and_xgboost_predictions_plot",
        ],
    )
