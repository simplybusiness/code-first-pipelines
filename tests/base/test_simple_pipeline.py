import time
from collections import Counter
from pathlib import Path
from unittest.mock import ANY

import pytest
from freezegun import freeze_time

from cf_pipelines.base.helper_classes import FunctionDetails, ProductLineage
from cf_pipelines.base.pipeline import Pipeline


@pytest.fixture
def simple_pipeline(parse_indented):
    simple = Pipeline("Simple Pipeline")

    @simple.step("step_1")
    def one():
        return {"artifact_1.txt": None}

    @simple.step("step_2")
    def two(*, artifact_1):
        return {"artifact_2.csv": None}

    @simple.step("step_3")
    def three(*, artifact_1, artifact_2):
        return {"artifact_3.png": None}

    return simple


def test_dependency_solver(simple_pipeline):
    expected_dependencies = {"two": {"one"}, "three": {"two", "one"}}
    actual_dependencies = simple_pipeline.solve_dependencies()

    assert expected_dependencies == actual_dependencies


def test_product_lineages(simple_pipeline):
    expected_lineages = {
        "artifact_1": ProductLineage(group="step_1", file_name="artifact_1.txt", produced_by="one"),
        "artifact_2": ProductLineage(group="step_2", file_name="artifact_2.csv", produced_by="two"),
        "artifact_3": ProductLineage(group="step_3", file_name="artifact_3.png", produced_by="three"),
    }
    assert expected_lineages == simple_pipeline.product_lineages


def test_function_details(simple_pipeline):
    expected_details = {
        "one": FunctionDetails(python_function=ANY, produces={"artifact_1"}, needs=set(), group="step_1"),
        "two": FunctionDetails(python_function=ANY, produces={"artifact_2"}, needs={"artifact_1"}, group="step_2"),
        "three": FunctionDetails(
            python_function=ANY, produces={"artifact_3"}, needs={"artifact_2", "artifact_1"}, group="step_3"
        ),
    }
    assert expected_details == simple_pipeline.function_details


@pytest.mark.parametrize(
    ["artifact_name", "path"],
    [
        ("artifact_1", Path(".pipelines/default/step_1/artifact_1.txt")),
        ("artifact_2", Path(".pipelines/default/step_2/artifact_2.csv")),
        ("artifact_3", Path(".pipelines/default/step_3/artifact_3.png")),
    ],
)
def test_get_artifacts(simple_pipeline, artifact_name, path):
    actual_path = simple_pipeline.get_local_artifact_path(artifact_name)
    assert actual_path == path


@freeze_time("2022-01-14 03:21:34")
@pytest.mark.parametrize(
    ["artifact_name", "path"],
    [
        ("artifact_1", Path(".pipelines/20220114032134000000/step_1/artifact_1.txt")),
        ("artifact_2", Path(".pipelines/20220114032134000000/step_2/artifact_2.csv")),
        ("artifact_3", Path(".pipelines/20220114032134000000/step_3/artifact_3.png")),
    ],
)
def test_get_artifacts_tracked(simple_pipeline, artifact_name, path):
    # We change the value of `track_all` here, but it is supposed to be set in the constructor of Pipeline
    simple_pipeline.track_all = True
    simple_pipeline.generate_run_id()

    actual_path = simple_pipeline.get_local_artifact_path(artifact_name)
    assert actual_path == path


def test_removes_data_for_function(simple_pipeline):
    function_to_delete = "two"
    artifact_from_function = "artifact_2"

    assert function_to_delete in simple_pipeline.function_details
    assert artifact_from_function in simple_pipeline.product_lineages

    simple_pipeline.clear_function_data(function_to_delete)

    assert function_to_delete not in simple_pipeline.function_details
    assert artifact_from_function not in simple_pipeline.product_lineages


def test_make_dag(simple_pipeline):
    # TODO: investigate what can be done to test DAG creation properly, at the moment, if the graph builds, we consider it done
    simple_pipeline.make_dag()


@pytest.fixture
def textual_pipeline(parse_indented, tmp_path):
    simple = Pipeline("Simple Pipeline", location=tmp_path)

    @simple.step("step_1")
    def hello():
        time.sleep(0.5)
        return {"artifact_1.txt": "Hello"}

    @simple.step("step_2")
    def world():
        return {"artifact_2.txt": "World"}

    @simple.step("step_3")
    def mix(*, artifact_1, artifact_2):
        return {"end.txt": artifact_1 + " " + artifact_2 + "!"}

    return simple


def test_execution(textual_pipeline: Pipeline, tmp_path):
    textual_pipeline.run()

    with open(tmp_path / "default" / "step_1" / "artifact_1.txt") as r:
        assert r.read() == "Hello"

    with open(tmp_path / "default" / "step_2" / "artifact_2.txt") as r:
        assert r.read() == "World"

    with open(tmp_path / "default" / "step_3" / "end.txt") as r:
        assert r.read() == "Hello World!"


def test_after_and_before_functions(textual_pipeline: Pipeline, tmp_path):
    counter = Counter()
    functions_results = dict()
    elapsed_time = 0.0

    def before_function(function_name):
        counter[function_name] += 1

    def after_function(function_name, results, run_time):
        nonlocal elapsed_time
        counter[function_name] += 1
        functions_results.update(results)
        elapsed_time += run_time

    textual_pipeline.set_after_function(after_function)
    textual_pipeline.set_before_step(before_function)

    textual_pipeline.run()

    assert counter == {"hello": 2, "world": 2, "mix": 2}
    assert functions_results == {"artifact_1": "Hello", "artifact_2": "World", "end": "Hello World!"}
    assert elapsed_time > 0.0
