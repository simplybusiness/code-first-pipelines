import ast
from unittest.mock import patch

import pytest


@pytest.fixture
def parse_indented():
    """
    This fixture enables the creation of pipelines whose source code exists nested inside another function's body
    """

    def parse_indented(source):
        first_at = source.find("@")
        lines = source.split("\n")
        final_source = "\n".join(line[first_at:] for line in lines)
        return ast.parse(final_source)

    with patch("cf_pipelines.base.utils.parse_source", parse_indented):
        yield
