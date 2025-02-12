from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    train_catboost_model,
    explain_catboost_model,
    plot_partial_dependence_catboost,
)

from ..random_forest_pipeline.nodes import (
    plot_real_data_and_predictions_with_train,
    plot_feature_importance,
    generate_predictions,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(  # Node 1: Train CatBoost Model
                func=train_catboost_model,
                inputs=[
                    "X_train",
                    "y_train",
                    "params:catboost_model_params",
                ],
                outputs="catboost_model",
                name="train_catboost_model_node",
                tags=["model_training", "catboost"],
            ),
            node(  # Node 2: Plot Feature Importance
                func=plot_feature_importance,
                inputs=[
                    "catboost_model",
                    "X_train",
                ],
                outputs="catboost_feature_importance_plot",
                name="plot_feature_importance_node",
                tags=[
                    "feature_importance",
                    "visualization",
                    "catboost",
                    "model_training",
                ],
            ),
            node(  # Node 3: Generate Predictions
                func=generate_predictions,
                inputs=[
                    "X_test",
                    "catboost_model",
                ],
                outputs="catboost_model_predictions",
                name="generate_predictions_node",
                tags=["predictions", "catboost", "model_training"],
            ),
            node(  # Node 4: Plot Real Data and Predictions
                func=plot_real_data_and_predictions_with_train,
                inputs=[
                    "y_train",
                    "y_test",
                    "catboost_model_predictions",
                ],
                outputs="real_data_and_catboost_predictions_plot",
                name="plot_real_data_and_predictions_node",
                tags=["data_visualization", "catboost", "model_training"],
            ),
            node(  # Node 5: Generate SHAP Summary Plot for Explainability
                func=explain_catboost_model,
                inputs=["catboost_model", "X_train"],
                outputs="catboost_shap_summary_plot",
                name="explain_catboost_model_node",
                tags=["explainability", "catboost", "model_training"],
            ),
            node(  # Node 7: Plot Partial Dependence
                func=plot_partial_dependence_catboost,
                inputs=["catboost_model", "X_train", "params:catboost_pdp_features"],
                outputs="catboost_partial_dependence_plot",
                name="plot_partial_dependence_node",
                tags=["partial_dependence", "catboost", "model_training"],
            ),
        ],
        tags="model_training",
        namespace="catboost_training_pipeline",
        inputs=["X_train", "y_train", "X_test", "y_test"],
        outputs=[
            "catboost_model",
            "catboost_feature_importance_plot",
            "real_data_and_catboost_predictions_plot",
            "catboost_shap_summary_plot",
            "catboost_partial_dependence_plot",
        ],
    )
