import warnings
from functools import wraps


def deprecated(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        warnings.warn(
            f"{fn.__name__} is deprecated and will be removed in the futur.",
            DeprecationWarning,
        )
        return fn(*args, **kwargs)

    return wrapped
