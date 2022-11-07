from typing import List


def split_segments(hl7_string: str) -> List[str]:
    return hl7_string.split("\n")
