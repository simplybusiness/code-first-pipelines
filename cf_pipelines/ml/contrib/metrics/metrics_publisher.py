from abc import ABC, abstractmethod
from typing import Any, List

from cf_pipelines.ml.contrib.metrics.models import Metric


class MetricsPublisher(ABC):
    @abstractmethod
    def publish(self, metric: Metric) -> None:
        pass


class CompositeMetricsPublisher(MetricsPublisher):
    def __init__(self, metrics_publishers: List[MetricsPublisher]) -> None:
        self.metrics_publishers = metrics_publishers

    def publish(self, metric: Metric) -> None:
        for publisher in self.metrics_publishers:
            publisher.publish(metric)
            publisher.publish(metric)


class MLFlowMetricsPublisher(MetricsPublisher):
    def __init__(self, mlflow: Any) -> None:
        self.mlflow = mlflow

    def publish(self, metric: Metric) -> None:
        self.mlflow.log_metrics(metric.as_dict())


class LocalMetricsPublisher(MetricsPublisher):
    def __init__(self) -> None:
        self.published_metrics: List[Metric] = []

    def publish(self, metric: Metric) -> None:
        self.published_metrics.append(metric)
