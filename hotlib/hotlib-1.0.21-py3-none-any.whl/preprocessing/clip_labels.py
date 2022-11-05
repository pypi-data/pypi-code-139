import os
from glob import glob
from pathlib import Path

import geopandas
from shapely.geometry import Polygon

from ..utils import get_bounding_box


def clip_labels(input_path: str, output_path: str, rasterize=False) -> None:
    """Clip the GeoJSON labels for each of the aerial images.

    For each of the OAM images, the corresponding GeoJSON file is
    clipped first. Then optionally, the clipped GeoJSON files are converted to TIFs.

    The EPSG:3857 projected coordinate system is used
    ('WGS 84 / Pseudo-Mercator', coordinates in meters).

    Args:
        input_path: Path of the directory where the input data are stored.
        output_path: Path of the directory where the output data will go.
    """
    os.makedirs(output_path, exist_ok=True)

    for path in glob(f"{input_path}/*.png"):
        filename = Path(path).stem
        x_min, y_min, x_max, y_max = get_bounding_box(filename)
        bounding_box = f"{x_min} {y_min} {x_max} {y_max}"

        orig_geojson_file = f"{input_path}/labels.geojson"
        clipped_geojson_file = f"{output_path}/{filename}.geojson"

        clip_labels = f"""
            ogr2ogr \
                -clipsrc {bounding_box} \
                -f GeoJSON {clipped_geojson_file} {orig_geojson_file}
        """
        os.system(clip_labels)

        if rasterize:
            raster_file = f"{output_path}/{filename}.tif"
            rasterize_labels = f"""
                gdal_rasterize \
                    -ot Byte \
                    -burn 255 \
                    -ts 256 256 \
                    -te {bounding_box} \
                    {clipped_geojson_file} {raster_file}
            """
            os.system(rasterize_labels)
