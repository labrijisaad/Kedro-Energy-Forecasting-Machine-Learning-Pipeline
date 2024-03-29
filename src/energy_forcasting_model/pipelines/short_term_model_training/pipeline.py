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
            node( # Node 1
                func=train_xgboost_model,
                inputs=[
                    "X_train_short_term_model",
                    "y_train_short_term_model",
                    "params:xgboost_model_params",
                ],
                outputs="short_term_xgboost_model",
                name="train_xgboost_model_node",
                tags=["model_training", "xgboost", "short_term_model_training"],
            ),
            node( # Node 2
                func=plot_feature_importance,
                inputs=[
                    "short_term_xgboost_model",
                    "X_train_short_term_model",
                ],
                outputs="xgboost_feature_importance_short_term_plot",
                name="plot_feature_importance_node",
                tags=[
                    "feature_importance",
                    "visualization",
                    "xgboost",
                    "short_term_model_training",
                ],
            ),
            node( # Node 3
                func=generate_predictions,
                inputs=[
                    "X_test_short_term_model",
                    "short_term_xgboost_model",
                ],
                outputs="short_term_xgboost_model_predictions",
                name="generate_predictions_node",
                tags=["predictions", "xgboost", "short_term_model_training"],
            ), 
            node( # Node 4
                func=plot_real_data_and_predictions_with_train,
                inputs=[
                    "y_train_short_term_model",
                    "y_test_short_term_model",
                    "short_term_xgboost_model_predictions",
                    "params:feature_splitting_short_term_model",
                ],
                outputs="real_data_and_xgboost_predictions_plot",
                name="plot_real_data_and_predictions_node",
                tags=["data_visualization", "xgboost", "short_term_model_training"],
            ),
        ],
        tags="short_term_model_training",
        namespace="short_term_model_training_pipeline",
        inputs=[
            "X_train_short_term_model", "y_train_short_term_model",
            "X_test_short_term_model", "y_test_short_term_model",
        ],
        outputs=[
            "short_term_xgboost_model",
            "xgboost_feature_importance_short_term_plot",
            "real_data_and_xgboost_predictions_plot",
        ],
    )
