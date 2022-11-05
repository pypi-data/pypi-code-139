from glob import glob

import rasterio as rio
from rasterio.merge import merge

CRS = "EPSG:4326"


def stitch(input_path: str, output_path: str):
    """Stitch GeoTIF files.

    Args:
        input_path: Path of the directory where the TIF files are stored.
        output_path: Path of the output file.
    """
    rasters = []
    for path in glob(f"{input_path}/*.tif"):
        raster = rio.open(path)
        rasters.append(raster)

    mosaic, output = merge(rasters)
    output_meta = raster.meta.copy()
    output_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": output,
        }
    )

    with rio.open(output_path, "w", **output_meta) as m:
        m.write(mosaic)
