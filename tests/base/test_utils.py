import pytest

from cf_pipelines.base.utils import remove_extension


@pytest.mark.parametrize(
    ["file_name", "expected_name"],
    [
        ("hello", "hello"),
        ("hello.txt", "hello"),
        ("hello.txt.gz", "hello"),
    ],
)
def test_remove_extension(file_name, expected_name):
    assert remove_extension(file_name) == expected_name
