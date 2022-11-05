from glob import glob

import numpy as np
import rasterio as rio
from geopandas import GeoSeries
from rasterio.features import shapes
from rasterio.merge import merge
from shapely.geometry import Polygon, shape

CRS = "EPSG:4326"
TOLERANCE = 1e-4


def vectorize(input_path: str, output_path: str):
    """Vectorize raster tiles.

    Args:
        input_path: Path of the directory where the TIF files are stored.
        output_path: Path of the output file.
    """
    rasters = []
    for path in glob(f"{input_path}/*.tif"):
        raster = rio.open(path)
        rasters.append(raster)

    mosaic, output = merge(rasters)
    polygons = [shape(s) for s, _ in shapes(mosaic, transform=output)]

    areas = [poly.area for poly in polygons]
    max_area, median_area = np.max(areas), np.median(areas)
    polygons = [
        Polygon(poly.exterior.coords)
        for poly in polygons
        if poly.area != max_area and poly.area > median_area / 10
    ]

    gs = GeoSeries(polygons).set_crs(CRS)
    gs.simplify(TOLERANCE).to_file(output_path)
