import logging
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Dict, Set, Union

import mlflow as global_mlflow
from ploomber.products import File

from cf_pipelines import Pipeline
from cf_pipelines.ml.contrib.metrics.metrics_publisher import MetricsPublisher
from cf_pipelines.ml.contrib.metrics.models import Metric, ModelEvaluationResult
from cf_pipelines.ml.contrib.mlflow_storage_client import MLflowStorageClient
from cf_pipelines.ml.drawing_utils import draw as draw_utils
from cf_pipelines.ml.machine_learning_step import MachineLearningStep

META_PREFIX = "meta"


class MLPipeline(Pipeline):
    """
    A specific implementation of a code-first pipeline

    Attributes
    __________
    name: str
        The name of the pipeline
    location: str or Path
        The pipelines store data locally for each run, with this parameter one can specify where this data is stored
    track_all: bool
        A flag that specifies whether each run should be tracked independently. When set to false, all the artifacts
        are saved to a "default" folder. If true, each run is saved to a unique folder identified by the time it ran
    registered_steps: Counter
        A counter to keep track of what steps of the ML pipeline have been registered to the pipeline
    mlflow: object
        An instance of MLflow
    """

    non_mandatory_steps = {MachineLearningStep.MODEL_DEPLOYMENT}

    def __init__(
        self,
        name: str,
        location: Union[str, Path] = ".pipelines",
        track_all: bool = False,
        user_mlflow: Any = None,
        metrics_publisher: MetricsPublisher = None,
        serializer: Callable = None,
        unserializer: Callable = None,
        extra_args: Dict[str, Any] = None,
    ):
        self.mlflow = user_mlflow or global_mlflow  # This probably should be an object, rather than the global mlflow
        self.metrics_publisher = metrics_publisher
        self.registered_steps: Counter = Counter()
        self.pipeline_logger = logging.getLogger(name)
        extra_args = extra_args or {}
        super().__init__(
            name=name,
            location=location,
            extra_args={"mlflow": self.mlflow, "logger": self.pipeline_logger, **extra_args},
            dag_clients={File: MLflowStorageClient(self.mlflow)},
            track_all=track_all,
            serializer=serializer,
            unserializer=unserializer,
        )

        self.set_after_function(self.ml_after_function)

    def step(self, step: MachineLearningStep) -> Callable:  # type: ignore[override]
        self.registered_steps[step] += 1
        return super().step(group=step.value)

    def clear_function_data(self, function_name: str) -> None:
        """
        Removes all data related to a given function, as well as decreasing the counter for that ML pipeline step

        :param function_name: The name of the function to delete
        """
        function_details = self.function_details[function_name]
        self.registered_steps[MachineLearningStep(function_details.group)] -= 1
        super().clear_function_data(function_name)

    def get_missing_steps(self) -> Set[MachineLearningStep]:
        """
        Calculate what are the steps that have not been registered to the pipeline
        :return: A set containing all the steps that have not been registered, therefore, if the set is empty, all
        steps exist within the pipeline
        """
        all_valid_steps = {step for step in MachineLearningStep} - MLPipeline.non_mandatory_steps
        actual_registered_steps = {step for step, count in self.registered_steps.items() if count > 0}
        return all_valid_steps - actual_registered_steps

    def ml_after_function(self, function_name: str, results: Dict[str, Any], elapsed_time: float) -> None:
        self.mlflow.log_param(f"{META_PREFIX}.{function_name}.time", elapsed_time)
        for key, result in results.items():
            if isinstance(result, ModelEvaluationResult):
                self.process_validation_result(result)

    def process_validation_result(self, model_evaluation: ModelEvaluationResult):

        if self.metrics_publisher:
            for metric in model_evaluation.metrics:
                self.metrics_publisher.publish(metric)

        failed_metrics = [metric for metric in model_evaluation.metrics if not metric.is_satisfied()]
        if failed_metrics:
            message = "\n".join([f"Unsatisfied metric {metric}" for metric in failed_metrics])
            self.meta_logger.error(message)
            raise RuntimeError(message)

    def draw(self, **kwargs):
        return draw_utils(self, **kwargs)

    def run(self, force=False) -> None:
        """
        Executes the pipeline
        :param force: If true, all the steps of the pipeline will be executed, even those whose source has not changed
        """

        if missing_steps := self.get_missing_steps():
            # The pipeline is missing some steps
            # TODO: Fail or log a warning, I don't think we should fail unless it is a production build
            pass

        self.mlflow.set_experiment(self.name)
        run_id = self.generate_run_id()
        with self.mlflow.start_run(run_name=run_id):
            self.make_dag().build(force=force)

    # These functions (or decorators) act as shorthands for the named steps we
    # want the ML Pipeline to have.

    def data_ingestion(self, scientist_fn=None):
        if not scientist_fn:
            return self.step(MachineLearningStep.DATA_INGESTION)
        else:
            return self.step(MachineLearningStep.DATA_INGESTION)(scientist_fn)

    def data_validation(self, scientist_fn=None):
        if not scientist_fn:
            return self.step(MachineLearningStep.DATA_VALIDATION)
        else:
            return self.step(MachineLearningStep.DATA_VALIDATION)(scientist_fn)

    def feature_engineering(self, scientist_fn=None):
        if not scientist_fn:
            return self.step(MachineLearningStep.FEATURE_ENGINEERING)
        else:
            return self.step(MachineLearningStep.FEATURE_ENGINEERING)(scientist_fn)

    def model_training(self, scientist_fn=None):
        if not scientist_fn:
            return self.step(MachineLearningStep.MODEL_TRAINING)
        else:
            return self.step(MachineLearningStep.MODEL_TRAINING)(scientist_fn)

    def model_testing(self, scientist_fn=None):
        if not scientist_fn:
            return self.step(MachineLearningStep.MODEL_TESTING)
        else:
            return self.step(MachineLearningStep.MODEL_TESTING)(scientist_fn)
