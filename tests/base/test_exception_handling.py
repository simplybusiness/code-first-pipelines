import pytest
from ploomber.exceptions import DAGBuildError

from cf_pipelines import Pipeline


@pytest.fixture
def simple_pipeline(parse_indented, tmp_path):
    simple = Pipeline("Simple Pipeline", location=tmp_path)

    @simple.step("step_1")
    def i_trow_an_exception():
        raise ValueError(":)")
        return {"artifact_1.txt": "Hello"}

    @simple.step("step_2")
    def world():
        return {"artifact_2.txt": "World"}

    return simple


def test_unhandled_error(simple_pipeline):
    with pytest.raises(DAGBuildError):
        simple_pipeline.run()


def test_handled_error(simple_pipeline):

    failed_function = ""

    def error_handler(function_name, exception, elapsed_time):
        nonlocal failed_function
        failed_function = function_name

    with pytest.raises(DAGBuildError):
        simple_pipeline.set_exception_handler(error_handler)
        simple_pipeline.run()

    assert failed_function
