from dataclasses import dataclass
from typing import Callable, Set


@dataclass
class FunctionDetails:
    """
    A class to hold details about a function: its reference, what artifacts it produces, which ones it generates
    and the group it belongs to.
    """

    python_function: Callable
    produces: Set[str]
    needs: Set[str]
    group: str


@dataclass
class ProductLineage:
    """
    A class to hold information about a given product (or artifact): the group it belongs to, the actual filename
    stored on disk and the name of the function that produces it.
    """

    group: str
    file_name: str
    produced_by: str
