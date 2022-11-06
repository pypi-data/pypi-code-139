from typing import Dict, Callable
from math import floor
import jwt
import functools
from datetime import datetime


def extend_headers(
    original_headers: Dict[str, str], extra_headers: Dict[str, str]
) -> Dict[str, str]:
    return {**original_headers, **extra_headers}


def jwt_authenticate(jwt_secret: str):
    def jwt_authenticate_decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def authenticate_request(*args, **kwargs):
            nonce = floor(datetime.now().timestamp())

            token = jwt.encode({"nonce": nonce}, jwt_secret)

            headers = kwargs.get("headers") or {}

            kwargs["headers"] = extend_headers(
                headers, {"Authorization": f"Bearer {token}"}
            )

            return func(*args, **kwargs)

        return authenticate_request

    return jwt_authenticate_decorator
