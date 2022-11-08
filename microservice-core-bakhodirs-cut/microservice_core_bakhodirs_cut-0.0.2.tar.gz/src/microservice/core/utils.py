import random
import string
from collections import defaultdict

from google.protobuf.json_format import ParseDict

from src.microservice.core.exceptions import ValidationException


def random_string(length_=10, additional_chars=" "):
    letters = string.ascii_lowercase + string.ascii_uppercase + additional_chars
    return "".join(random.choice(letters) for _ in range(length_))


def _check_request(request, fields):
    errors = defaultdict(list)
    for field in fields:
        if not getattr(request, field):
            errors["invalid_arguments"].append(f"Field {field} is required")

    if errors:
        raise ValidationException(errors)


def convert(data, pb):
    try:
        return pb(**data)
    except Exception:
        return ParseDict(data, pb(), ignore_unknown_fields=True)



