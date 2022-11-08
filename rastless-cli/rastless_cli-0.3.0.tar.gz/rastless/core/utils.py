from typing import List


def merge_bbox_extent(bboxes: List) -> List:
    bboxes = list(map(list, zip(*bboxes)))

    return [min(bboxes[0]), min(bboxes[1]), max(bboxes[2]), max(bboxes[3])]

