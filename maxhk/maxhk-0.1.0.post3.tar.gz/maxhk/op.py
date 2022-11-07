from collections import namedtuple
from typing import List
import json
import re
import shutil
import subprocess as sp

def __check_op() -> None:
    if shutil.which("op") is None:
        raise RuntimeError("`op` is not installed")


def _build_id(entry):
    section = entry.get("section", {}).get("label")
    new_id = "_".join([section, entry.get("label")]) if section else entry.get("label")
    return  re.sub('[^\w]', '_', new_id)


def _get_item(item_id: str) -> dict:
    __check_op()
    raw_data = sp.getoutput(f"op item get {item_id} --format json")
    data = json.loads(raw_data).get("fields", [])
    return {_build_id(x): x.get("value") for x in data}


def get_item(item_id: str, fields: List[str] = None) -> namedtuple:
    """Retrieves an item from 1password.

    Keyword arguments:
    item_id -- first parameter to `op item get`.
    fields  -- fields to include in the result tuple. All fields are included
    when this argument is None or empty.
    """
    __check_op()
    fields = fields or []
    data = _get_item(item_id)
    all_fields = set(data)
    missing_fields = set(fields) - all_fields
    if missing_fields:
        raise KeyError("Missing fields: %s" % ", ".join(missing_fields))
    fields_to_return = fields or all_fields
    ResultType = namedtuple("Item", fields or fields_to_return)
    return ResultType(**{k: v for (k, v) in data.items() if k in fields_to_return})
