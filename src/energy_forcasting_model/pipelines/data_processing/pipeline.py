from kedro.pipeline import Pipeline, node, pipeline

from .nodes import transform_data, import_data_1, import_data_2, import_data_3


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=import_data_1,
                inputs="jours_feries_metropole",
                outputs="jours_feries_metropole2",
                name="import_data_1",
            ),
            node(
                func=import_data_2,
                inputs="sceaux_data_part1",
                outputs="sceaux_data_part11",
                name="import_data_2",
            ),
            node(
                func=import_data_3,
                inputs="sceaux_data_part2",
                outputs="sceaux_data_part22",
                name="import_data_3",
            ),
            node(
                func=transform_data,
                inputs=[
                    "jours_feries_metropole2",
                    "sceaux_data_part11",
                    "sceaux_data_part22",
                ],
                outputs="transformed_data",
                name="transform_data",
            ),
        ]
    )
