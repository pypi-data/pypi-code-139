from typing import Any, List, Optional, Union


def is_array(data: Optional[Union[Any, List[Any]]]) -> bool:
    if data and isinstance(data, list):
        return True
    return False
