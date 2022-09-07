from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


class Expectation(ABC):
    def __init__(self, expected_value: float) -> None:
        self.expected_value = expected_value

    @abstractmethod
    def is_satisfied(self, value: float) -> bool:
        pass

    def __repr__(self):
        return f"{type(self).__name__}({self.expected_value})"

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Expectation):
            return self.expected_value == obj.expected_value
        else:
            return False


class GreaterThan(Expectation):
    def is_satisfied(self, value: float) -> bool:
        return value >= self.expected_value

    def __str__(self) -> str:
        return f"greater than {self.expected_value}"


class LowerThan(Expectation):
    def is_satisfied(self, value: float) -> bool:
        return value <= self.expected_value

    def __str__(self) -> str:
        return f"lower than {self.expected_value}"


class Metric:
    def __init__(self, name: str, value: float, expectation: Expectation):
        self.name = name
        self.value = value
        self.expectation = expectation

    def is_satisfied(self) -> bool:
        return self.expectation.is_satisfied(self.value)

    def as_dict(self) -> Dict[str, float]:
        return {self.name: self.value}

    def __str__(self) -> str:
        return f"Metric {self.name} with value {self.value} expected to be {self.expectation}"

    def __repr__(self):
        return f'Metric("{self.name}", {self.value}, {repr(self.expectation)})'

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Metric):
            return self.name == obj.name and self.expectation == obj.expectation
        else:
            return False


class ModelEvaluationResult:
    def __init__(self, metrics: Optional[List[Metric]] = None) -> None:
        self.metrics: List[Metric] = metrics or []
        self.conditions: List[Callable] = []

    def metric(self, metric: Metric) -> "ModelEvaluationResult":
        self.metrics.append(metric)
        return self

    def condition(self, condition: Callable) -> "ModelEvaluationResult":
        self.conditions.append(condition)
        return self
