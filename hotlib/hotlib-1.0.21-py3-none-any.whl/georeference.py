import os
from glob import glob
from pathlib import Path

from .utils import get_bounding_box


def georeference(input_path: str, output_path: str, is_mask=False) -> None:
    """Perform georeferencing and remove the fourth band from images (if any).

    If the image has only one band, that fourth band removal part
    will be skipped.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_path: Path of the directory where the input data are stored.
        output_path: Path of the directory where the output data will go.
        is_mask: Whether the image is binary or not.
    """
    os.makedirs(output_path, exist_ok=True)

    for path in glob(f"{input_path}/*.png"):
        filename = Path(path).stem
        x_min, y_min, x_max, y_max = get_bounding_box(filename)
        bounding_box = f"{x_min} {y_max} {x_max} {y_min}"

        process_image = f"""
            gdal_translate \
                -b 1 {'' if is_mask else '-b 2 -b 3'} \
                -a_ullr {bounding_box} \
                -a_srs EPSG:3857 \
                {input_path}/{filename}.png \
                {output_path}/{filename}.tif
        """
        os.system(process_image)
