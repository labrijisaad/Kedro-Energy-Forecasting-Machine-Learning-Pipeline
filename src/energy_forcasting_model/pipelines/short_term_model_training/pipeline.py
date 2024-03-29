from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    create_features,
    prepare_train_test_sets,
    train_test_split_plot,
    train_xgboost_model,
    plot_feature_importance,
    plot_real_data_and_predictions,
)

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
            node(
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
            node(
                func=plot_feature_importance,
                inputs=[
                    "short_term_xgboost_model",
                    "X_train_short_term_model", 
                ],
                outputs="xgboost_feature_importance_short_term_plot",
                name="plot_feature_importance_node",
                tags=["feature_importance", "visualization", "xgboost", "short_term_model_training"],
            ),
            node(
                func=plot_real_data_and_predictions,
                inputs=["X_test_short_term_model", 
                       "y_test_short_term_model", 
                       "short_term_xgboost_model", 
                       "params:feature_splitting_short_term_model"],
                outputs="real_data_and_xgboost_predictions_plot",
                name="plot_real_data_and_predictions_node",
                tags=["data_visualization", "xgboost", "short_term_model_training"],
            ),

        ],
        tags="short_term_model_training",
        namespace="short_term_model_training",
        inputs="processed_weather_and_consumption_data",
        outputs=["train_test_split_visualization",
                 "short_term_xgboost_model",
                 "xgboost_feature_importance_short_term_plot",
                 "real_data_and_xgboost_predictions_plot"]
    )
