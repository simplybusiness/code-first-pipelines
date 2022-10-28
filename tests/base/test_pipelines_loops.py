import pytest

from cf_pipelines import Pipeline
from cf_pipelines.exceptions import CycledPipelineError


@pytest.fixture
def simple_looped_pipeline(parse_indented):
    simple = Pipeline("Simple Pipeline")

    @simple.step("step_1")
    def one(*, one):
        return {"one.txt": None}

    return simple


@pytest.fixture
def looped_pipeline(parse_indented):
    simple = Pipeline("Simple Pipeline")

    @simple.step("step")
    def f_one():
        return {"two.txt": None}

    @simple.step("step")
    def f_two(*, two, four):
        return {"three.txt": None}

    @simple.step("step")
    def f_three(*, three):
        return {"four.txt": None}

    return simple


@pytest.mark.parametrize("pipeline", ["simple_looped_pipeline", "looped_pipeline"])
def test_make_dag_fail_when_looped(pipeline, request):
    actual_pipeline = request.getfixturevalue(pipeline)

    with pytest.raises(CycledPipelineError):
        actual_pipeline.make_dag()
