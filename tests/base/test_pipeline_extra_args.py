import os
from unittest.mock import patch

import pytest

from cf_pipelines import Pipeline


def test_fails_if_when_arg_is_not_passed(parse_indented):
    pipeline = Pipeline("hello")

    @pipeline.step("foo")
    def step_one(*, hello, world):
        return {"pass": None}

    with pytest.raises(KeyError):
        pipeline.solve_dependencies()


def test_passes_args_from_constructor(parse_indented, tmp_path):
    pipeline = Pipeline("hello", extra_args={"hello": "hola", "world": "mundo"}, location=tmp_path)

    @pipeline.step("foo")
    def step_one(*, hello, world):
        return {"text": f"{hello} {world}"}

    @pipeline.step("bar")
    def step_two(*, text):
        return {"result.txt": text}

    pipeline.run()

    actual_result = open(tmp_path / "default" / "bar" / "result.txt").read()
    assert actual_result == "hola mundo"


def test_passes_args_from_environment_variables(parse_indented, tmp_path):
    pipeline = Pipeline("hello", location=tmp_path)

    @pipeline.step("foo")
    def step_one(*, hello, world):
        return {"text": f"{hello} {world}"}

    @pipeline.step("bar")
    def step_two(*, text):
        return {"result.txt": text}

    with patch.dict(os.environ, {"CF_HELLO": "hola", "CF_WORLD": "mundo"}):
        pipeline.run()

    actual_result = open(tmp_path / "default" / "bar" / "result.txt").read()
    assert actual_result == "hola mundo"


def test_assert_argument_precedence(parse_indented, tmp_path):
    pipeline = Pipeline("hello", extra_args={"hello": "hola", "world": "mundo"}, location=tmp_path)

    @pipeline.step("foo")
    def step_one(*, hello, world):
        return {"text": f"{hello} {world}"}

    @pipeline.step("bar")
    def step_two(*, text):
        return {"result.txt": text}

    with patch.dict(os.environ, {"CF_HELLO": "ciao", "CF_WORLD": "mondo"}):
        pipeline.run()

    actual_result = open(tmp_path / "default" / "bar" / "result.txt").read()
    assert actual_result == "ciao mondo"
