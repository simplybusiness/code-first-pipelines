import pytest

from cf_pipelines.base.utils import get_return_keys_from_function


def no_return_statement():
    pass


def return_string():
    return "hello"


def returns_empty_dictionary():
    return {}


@pytest.mark.parametrize(
    "function",
    [
        no_return_statement,
        return_string,
        returns_empty_dictionary,
    ],
    ids=["no return statement", "returns a string", "returns empty dictionary"],
)
def test_get_return_keys_from_function_fails(function):
    with pytest.raises(ValueError):
        get_return_keys_from_function(function)


def return_single_key():
    return {"hello.txt": "world"}


def return_multiple_keys():
    return {"hello.txt": "world", "hello.png": "world", "hello": "world"}


@pytest.mark.parametrize(
    ["function", "expected_keys"],
    [
        (return_single_key, ["hello.txt"]),
        (return_multiple_keys, ["hello.txt", "hello.png", "hello"]),
    ],
    ids=["single key", "multiple keys"],
)
def test_get_return_keys_from_function_succeeds(function, expected_keys):
    actual = get_return_keys_from_function(function)
    assert expected_keys == actual
