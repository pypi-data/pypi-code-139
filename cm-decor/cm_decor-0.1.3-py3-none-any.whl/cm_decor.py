from contextlib import ExitStack
from functools import wraps


def exitstack(name: str):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kw):
            with ExitStack() as stack:
                kw[name] = stack
                return fn(*args, **kw)

        return wrapper

    return decorate


cm = exitstack('cm')