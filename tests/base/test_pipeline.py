import pytest

from cf_pipelines.base.helper_classes import FunctionDetails, ProductLineage
from cf_pipelines.base.pipeline import Pipeline


def test_add_product_lineages():
    pipeline = Pipeline("test")

    expected = {
        "machine": ProductLineage(group="data_ingestion", file_name="machine.txt", produced_by="original function"),
        "learning": ProductLineage(group="data_ingestion", file_name="learning.txt", produced_by="original function"),
    }

    assert not pipeline.product_lineages

    pipeline.add_product_lineages(
        "original function",
        [
            "machine.txt",
            "learning.txt",
        ],
        "data_ingestion",
    )

    assert pipeline.product_lineages == expected


def test_add_function_details():
    pipeline = Pipeline("test")

    assert not pipeline.function_details

    def some_function():
        pass

    expected = {
        "other_function": FunctionDetails(
            python_function=some_function, produces={"values", "return"}, needs={"pencils", "books"}, group="my_group"
        )
    }

    pipeline.add_function_details(
        some_function, {"books", "pencils"}, "other_function", ["return", "values"], group="my_group"
    )

    assert pipeline.function_details == expected


def test_solve_dependencies_fails_because_parameter_is_not_available(parse_indented):
    pipeline = Pipeline("test")

    @pipeline.step("first_step")
    def cool_function(*, these, argument, doesnt, exist):
        return {"result": 1}

    with pytest.raises(KeyError):
        pipeline.solve_dependencies()


def test_function_can_be_called_directly(parse_indented):
    pipeline = Pipeline("test")

    @pipeline.step("sum")
    def sum_the_numbers(*, a, b):
        return {"result": a + b}

    @pipeline.step("get_numbers")
    def generate_numbers():
        return {"a": 1, "b": 2}

    sum_results = sum_the_numbers(a=1, b=2)
    generate_numbers_results = generate_numbers()

    assert sum_results["result"] == 3
    assert generate_numbers_results["a"] == 1
    assert generate_numbers_results["b"] == 2
