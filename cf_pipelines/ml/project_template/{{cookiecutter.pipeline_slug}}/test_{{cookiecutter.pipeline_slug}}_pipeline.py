import pandas as pd
from {{cookiecutter.pipeline_slug}}_pipeline import create_feature_interactions


def test_create_feature_interactions():
    input_data = pd.DataFrame({"sepal length (cm)": [1, 2], "sepal width (cm)": [3, 4]})
    expected = pd.DataFrame({"sepal area (cm2)": [3, 8]})

    results = create_feature_interactions(raw_data=input_data)

    engineered_features = results["engineered_features.csv"]
    pd.testing.assert_frame_equal(expected, engineered_features)
