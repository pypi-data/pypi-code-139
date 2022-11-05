import geopandas
from shapely.validation import explain_validity, make_valid


def remove_self_intersection(row):
    """Fix self-intersections in the polygons.

    Some of the polygons may have self-intersections. In that
    case, we transform that geometry to a multi-polygon and
    substitute the original geometry with the largest polygon.
    """
    if explain_validity(row.geometry) == "Valid Geometry":
        return row.geometry

    valid_geom = make_valid(row.geometry)
    if not hasattr(valid_geom, "__len__"):
        return valid_geom

    for polygon in valid_geom.geoms:
        if polygon.area >= row.geometry.area / 2.0:
            return polygon


def fix_labels(input_path: str, output_path: str) -> None:
    """Fix GeoJSON file so that it doesn't have any self-intersecting polygons.

    Also, convert the CRS of a GeoJSON file from EPSG:4326 to EPSG:3857.

    The new GeoJSON file contains coordinates in meters (east, north)
    in the 'WGS 84 / Pseudo-Mercator' projection.

    Args:
        input_path: Path of the input file.
        output_path: Path of the output file.
    """
    gdf = geopandas.read_file(input_path).set_crs("EPSG:4326")
    gdf["geometry"] = gdf.apply(remove_self_intersection, axis=1)
    gdf = gdf.to_crs("EPSG:3857")
    gdf.to_file(output_path)
