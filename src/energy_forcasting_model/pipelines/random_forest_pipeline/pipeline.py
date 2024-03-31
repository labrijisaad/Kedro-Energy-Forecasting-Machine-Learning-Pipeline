from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    generate_predictions,
    plot_real_data_and_predictions_with_train,
    train_random_forest_model,
    plot_feature_importance,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_random_forest_model,
                inputs=["X_train", "y_train", "params:random_forest_model_params"],
                outputs="random_forest_model",
                name="train_random_forest_model_node",
                tags=["random_forest", "model_training"],
            ),
            node(
                func=plot_feature_importance,
                inputs=["random_forest_model", "X_train"],
                outputs="random_forest_feature_importance_plot",
                name="plot_rf_feature_importance_node",
                tags=["random_forest", "feature_importance"],
            ),
            node(
                func=generate_predictions,
                inputs=["X_test", "random_forest_model"],
                outputs="rf_predictions",
                name="generate_rf_predictions_node",
                tags=["random_forest", "predictions"],
            ),
            node(
                func=plot_real_data_and_predictions_with_train,
                inputs=[
                    "y_train",
                    "y_test",
                    "rf_predictions",
                ],
                outputs="real_data_and_rf_predictions_plot",
                name="plot_real_data_and_rf_predictions_node",
                tags=["random_forest", "data_visualization"],
            ),
        ],
        tags="random_forest_pipeline",
        namespace="random_forest_pipeline",
        inputs=[
            "X_train",
            "y_train",
            "X_test",
            "y_test",
        ],
        outputs=[
            "random_forest_model",
            "random_forest_feature_importance_plot",
            "real_data_and_rf_predictions_plot",
        ],
    )
