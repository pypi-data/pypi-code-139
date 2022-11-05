from collections import namedtuple
from typing import List
import json
import shutil
import subprocess as sp


def __check_op() -> None:
    if shutil.which("op") is None:
        raise RuntimeError("`op` is not installed")


def get_item(item_id: str, fields: List[str]) -> namedtuple:
    __check_op()
    ResultType = namedtuple("Item", fields)
    csv_fields = ",".join(fields)
    data = sp.getoutput(f'op item get {item_id} --format json --fields "{csv_fields}"')
    return ResultType(*[x["value"] for x in json.loads(data)])
