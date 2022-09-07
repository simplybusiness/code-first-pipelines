import inspect
from functools import wraps

from cf_pipelines.base.utils import wrap_preserving_signature


def test_wrap_preserving_signature():
    def wrapper(wrapped):
        def _wrapper(cool, inner, arguments):
            """Wrapped docs"""
            pass

        # The actual execution of our function
        wrap_preserving_signature(_wrapper, wrapped)
        return _wrapper

    @wrapper
    def function(some, other, arguments):
        """My cool wrapped function"""

    assert function.__name__ == "function"
    assert function.__doc__ == "My cool wrapped function"
    function_signature = inspect.signature(function)
    assert set(function_signature.parameters.keys()) == {"cool", "inner", "arguments"}


def test_wrap_using_wraps():
    """This tests acts as a counter example of `test_wrap_preserving_signature` to show the undesired effect of @wraps"""

    def wrapper(wrapped):
        @wraps(wrapped)
        def _wrapper(cool, inner, arguments):
            """Wrapped docs"""
            pass

        # Notice, instead of `wrap_preserving_signature` we are using `@wraps`.
        return _wrapper

    @wrapper
    def function(some, other, arguments):
        """My cool wrapped function"""

    assert function.__name__ == "function"
    assert function.__doc__ == "My cool wrapped function"
    function_signature = inspect.signature(function)
    # The signature of the function is the same as `function`
    assert set(function_signature.parameters.keys()) == {"some", "other", "arguments"}
