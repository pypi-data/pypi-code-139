from contextlib import ExitStack
from dataclasses import dataclass
from functools import wraps


@dataclass
class InExitStack:
    name: str

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kw):
            with ExitStack() as stack:
                kw[self.name] = stack
                return fn(*args, **kw)

        return wrapper


cm = InExitStack('cm')