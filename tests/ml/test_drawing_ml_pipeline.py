import pytest

from cf_pipelines.ml.drawing_utils import draw
from cf_pipelines.ml.ml_pipeline import MLPipeline


@pytest.fixture
def simple_pipeline(parse_indented):
    simple = MLPipeline("Simple Pipeline")

    @simple.data_ingestion
    def number1():
        return {"n1": 4}

    @simple.data_ingestion
    def number2():
        return {"n2": 2}

    @simple.data_ingestion
    def test_data():
        return {"n4": 7}

    @simple.data_validation
    def validate(*, n1, n2):
        return {"valid.txt": "The numbers are valid"}

    @simple.feature_engineering
    def multiplied(*, n1, n2):
        return {"n3": n1 * n2}

    @simple.model_training
    def training(*, n1, n2, n3):
        return {"model": n1 * n2 * n3}

    @simple.model_testing
    def model_testing(*, model, n4):
        return {"hello": "world"}

    return simple


@pytest.mark.skip(reason="we can't test this currently")
def test_draw(simple_pipeline: MLPipeline):
    m = draw(simple_pipeline)
