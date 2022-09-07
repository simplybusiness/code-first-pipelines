import ast
import inspect
from ast import parse as parse_source
from functools import update_wrapper
from typing import Any, Callable, List, no_type_check


@no_type_check
def get_return_keys_from_function(function: Callable) -> List[str]:
    """
    Parses the source code of `function` in search for a return dict() statement. Useful to find the names of the
    products a function returns.

    :param function: The function to parse
    :return: A list with the keys of the return dictionary
    """
    source = inspect.getsource(function)
    function_source = parse_source(source)

    # function_source.body[0].body[-1] refers to the last statement of the function's body, which for our purposes
    # should be a dictionary
    if not isinstance(function_source.body[0].body[-1], ast.Return):
        raise ValueError(f"Function {function.__name__} does not have a return clause")
    if not isinstance(function_source.body[0].body[-1].value, ast.Dict):
        raise ValueError(f"Function {function.__name__} does not return a dictionary")
    return_keys = [key.value for key in function_source.body[0].body[-1].value.keys]
    if not return_keys:
        raise ValueError(f"Function {function.__name__} does not return any value")
    return return_keys


def wrap_preserving_signature(wrapper_fn: Callable, inner_fn: Any) -> None:
    """
    Copies all the metadata from `inner_fn` to `wrapper_fn`, with the exception of `wrapper_fn`'s signature.
    The `@wraps` decorator could have been used instead, but it overrides the function's signature, which is not
    something we desire.

    :param wrapper_fn:
    :param inner_fn:
    """
    inner_signature = inspect.signature(wrapper_fn)
    update_wrapper(wrapper_fn, inner_fn)
    inner_fn.__signature__ = inner_signature


def remove_extension(file_name: str) -> str:
    """
    Remove the extension from a file name and return only the stem

    :param file_name:
    :return:
    """
    return file_name.partition(".")[0]
