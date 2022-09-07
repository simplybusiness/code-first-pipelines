import pytest
from ploomber.exceptions import DAGBuildError

from cf_pipelines.ml.contrib.metrics.metrics_publisher import LocalMetricsPublisher
from cf_pipelines.ml.contrib.metrics.models import GreaterThan, Metric, ModelEvaluationResult
from cf_pipelines.ml.machine_learning_step import MachineLearningStep
from cf_pipelines.ml.ml_pipeline import MLPipeline


def test_doesnt_have_any_steps():
    pipeline = MLPipeline("A machine learning pipeline")
    assert pipeline.get_missing_steps()


def test_doesnt_have_all_steps(parse_indented):
    pipeline = MLPipeline("A machine learning pipeline")

    @pipeline.data_ingestion
    def ingest_data(*, _):
        return {"thing": None}

    @pipeline.data_validation()
    def ingest_data(*, thing):
        return {"thing2": None}

    assert pipeline.get_missing_steps()


def test_has_all_steps(parse_indented):
    pipeline = MLPipeline("A machine learning pipeline")

    @pipeline.data_ingestion
    def ingest_data(*, _):
        return {"thing": None}

    @pipeline.data_validation
    def validate_data(*, thing):
        return {"thing2": None}

    @pipeline.feature_engineering
    def feature_engineering(*, thing):
        return {"thing2": None}

    @pipeline.model_training
    def model_training(*, thing):
        return {"thing2": None}

    @pipeline.model_testing
    def model_testing(*, thing):
        return {"thing2": None}

    assert not pipeline.get_missing_steps()


def test_remove_function(parse_indented):
    pipeline = MLPipeline("A machine learning pipeline")

    @pipeline.data_ingestion
    def ingest_data():
        return {"thing": None}

    assert pipeline.registered_steps == {MachineLearningStep.DATA_INGESTION: 1}

    pipeline.clear_function_data(ingest_data.__name__)

    assert pipeline.registered_steps == {MachineLearningStep.DATA_INGESTION: 0}


def test_validate_metrics_fails(parse_indented, tmp_path):
    pipeline = MLPipeline("A machine learning pipeline", location=tmp_path)

    @pipeline.data_ingestion
    def data_ingestion():
        return {"data": 0.5}

    @pipeline.data_validation
    def validate_model_2(*, data):
        return {"evaluation.json": ModelEvaluationResult([Metric(name="f1", value=data, expectation=GreaterThan(0.6))])}

    with pytest.raises(DAGBuildError) as dag_build_error:
        pipeline.run()


def test_validate_function_passes(parse_indented, tmp_path):
    pipeline = MLPipeline("A machine learning pipeline", location=tmp_path)

    @pipeline.data_ingestion
    def data_ingestion():
        return {"data": 0.9}

    @pipeline.data_validation
    def validate_model_2(*, data):
        return {"evaluation.json": ModelEvaluationResult([Metric(name="f1", value=data, expectation=GreaterThan(0.6))])}

    pipeline.run()


def test_metric_publisher(parse_indented, tmp_path):

    expected_metrics = [Metric("f1", 0.9, GreaterThan(0.6)), Metric("accuracy", 0.9, GreaterThan(0.6))]

    local_metrics_publisher = LocalMetricsPublisher()
    pipeline = MLPipeline("A machine learning pipeline", metrics_publisher=local_metrics_publisher, location=tmp_path)

    @pipeline.data_ingestion
    def data_ingestion():
        return {"data": 0.9}

    @pipeline.data_validation
    def validate_model_2(*, data):
        return {
            "metrics.json": ModelEvaluationResult(
                [
                    Metric(name="f1", value=data, expectation=GreaterThan(0.6)),
                    Metric(name="accuracy", value=data, expectation=GreaterThan(0.6)),
                ]
            )
        }

    pipeline.run()

    assert local_metrics_publisher.published_metrics == expected_metrics
