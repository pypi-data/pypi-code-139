from functools import wraps

from ffed.custom_exceptions import MutuallyExclusiveOptionsException


def add_dynamic_docstring(docstring_function):
    """
    - decorator to add dynamic docstring to a function.
    - Useful for functions which have similar docstrings or need to run some sort of code to include certain keywords in
      docstring
    :param docstring_function: function that returns the docstring
    :return: decorator
    """

    def decorator(func):
        func.__doc__ = docstring_function()

        @wraps(func)
        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)

            return return_value

        return wrapper

    return decorator


def mutually_exclusive_options(*options):
    """
    - decorator to define mutually exclusive options of click subcommand
    :param options:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            option_values = {key: kwargs[key] for key in options if kwargs[key]}

            if not option_values:
                raise MutuallyExclusiveOptionsException(
                    f"At-least one option is required from {','.join(options)}"
                )

            if len(option_values) > 1:
                raise MutuallyExclusiveOptionsException(
                    f"For mutually exclusive options ({','.join(options)}) only one is required"
                )

            for i in options:
                kwargs.pop(i)
            return_value = func(*args, **kwargs, **option_values)

            return return_value

        return wrapper

    return decorator
