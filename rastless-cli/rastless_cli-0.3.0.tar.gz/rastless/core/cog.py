from rio_cogeo.cogeo import cog_validate, cog_info, cog_translate
import boto3
from dataclasses import dataclass
from rasterio.io import MemoryFile
from rio_cogeo.profiles import cog_profiles
from typing import List, Set, TYPE_CHECKING
from pyproj import Transformer
import os
import click
from decimal import Decimal

from rastless.db.models import LayerStepModel
from rastless.core.utils import merge_bbox_extent

if TYPE_CHECKING:
    from rastless.config import Cfg


@dataclass
class S3Cog:
    filename: str
    bucket_name: str
    s3_object_name: str
    s3_path: str
    filepath: str = None


@dataclass
class LayerInfo:
    bbox_wgs84: List[float]
    resolution: float
    minzoom: int
    maxzoom: int


def create_s3_cog_info(bucket_name: str, layer_id: str, datetime: str, filepath: str) -> S3Cog:
    filename = os.path.basename(filepath)
    object_name = f"layer/{layer_id}/{datetime}/{filename}"
    s3_path = f"s3://{bucket_name}/{object_name}"
    return S3Cog(s3_object_name=object_name, s3_path=s3_path, bucket_name=bucket_name, filename=filename,
                 filepath=filepath)


def get_s3_cog_info_from_s3_path(s3_file_path: str) -> S3Cog:
    parts = s3_file_path.split("/")
    object_name = "/".join(parts[3:])
    return S3Cog(s3_object_name=object_name, s3_path=s3_file_path, bucket_name=parts[2], filename=parts[-1])


def upload_cog_file(s3_cog: S3Cog) -> bool:
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(s3_cog.filepath, s3_cog.bucket_name, s3_cog.s3_object_name)
    except Exception:
        return False
    return True


def transform_upload_cog(s3_cog: S3Cog, cog_profile: str) -> bool:
    s3_client = boto3.client("s3")
    dst_profile = cog_profiles.get(cog_profile)

    try:
        with MemoryFile() as mem_dst:
            cog_translate(s3_cog.filepath, mem_dst.name, dst_profile, in_memory=True, web_optimized=True)
            s3_client.upload_fileobj(mem_dst, s3_cog.bucket_name, s3_cog.s3_object_name)
    except Exception:
        return False
    return True


def layer_is_valid_cog(filepath: str) -> bool:
    result = cog_validate(filepath, quiet=True)
    return result == (True, [], [])


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def transform_bbox(bbox, in_proj: str, out_proj: str = "EPSG:4326") -> List[float]:
    transformer = Transformer.from_crs(in_proj, out_proj, always_xy=True)

    if in_proj == "EPSG:4326":
        bbox_wgs84_array = bbox
    else:
        bbox_wgs84 = [transformer.transform(x, y) for x, y in pairwise(bbox)]
        bbox_wgs84_array = list(sum(bbox_wgs84, ()))

    return bbox_wgs84_array


def get_layer_info(filename: str) -> LayerInfo:
    result = cog_info(filename)
    geo_info = result["GEO"]
    bbox_wgs84 = transform_bbox(geo_info["BoundingBox"], geo_info["CRS"])
    bbox_wgs84 = [round(x, 6) for x in bbox_wgs84]

    return LayerInfo(bbox_wgs84=bbox_wgs84, resolution=float(geo_info["Resolution"][0]),
                     maxzoom=geo_info["MaxZoom"], minzoom=geo_info["MinZoom"])


def upload_files(cfg: 'Cfg', filenames: Set[str], layer_id: str, datetime: str, profile: str, cog_filepaths: Set[str],
                 bboxes: List, resolutions: List) -> (Set[str], List[float], float):
    for filename in filenames:
        s3_cog = create_s3_cog_info(cfg.s3.bucket_name, layer_id, datetime, filename)
        layer_info = get_layer_info(filename)

        if layer_is_valid_cog(filename):
            uploaded = upload_cog_file(s3_cog)
        else:
            uploaded = transform_upload_cog(s3_cog, profile)

        if uploaded:
            cog_filepaths.add(s3_cog.s3_path)
            bboxes.append(layer_info.bbox_wgs84)
            resolutions.append(layer_info.resolution)
        else:
            raise click.echo(f"File {filename} could not be uploaded. Please try again.")

    bbox_extent = merge_bbox_extent(bboxes)

    return cog_filepaths, bbox_extent, min(resolutions)


def create_new_timestep(cfg: 'Cfg', filenames: Set[str], layer_id: str, datetime: str, profile: str,
                        temporal_resolution: str, sensor: str):
    cog_filepaths = set()
    bboxes = []
    resolutions = []

    cog_filepaths, bbox_extent, resolution = upload_files(cfg, filenames, layer_id, datetime, profile, cog_filepaths,
                                                          bboxes, resolutions)

    layer_step = LayerStepModel(layer_id=layer_id, cog_filepaths=cog_filepaths, datetime=datetime, sensor=sensor,
                                temporal_resolution=temporal_resolution, maxzoom=22,
                                minzoom=0,
                                bbox=bbox_extent, resolution=Decimal(resolution))
    cfg.db.add_layer_step(layer_step)


def append_to_timestep(cfg: 'Cfg', layer_step: LayerStepModel, filenames: Set[str], profile: str):
    cog_filepaths = layer_step.cog_filepaths if layer_step.cog_filepaths else {layer_step.cog_filepath}
    bboxes = [layer_step.bbox]
    resolutions = [layer_step.resolution]

    cog_filepaths, bbox_extent, resolution = upload_files(cfg, filenames, layer_step.layer_id, layer_step.datetime,
                                                          profile, cog_filepaths, bboxes, resolutions)

    layer_step = LayerStepModel(layer_id=layer_step.layer_id, cog_filepaths=cog_filepaths, datetime=layer_step.datetime,
                                sensor=layer_step.sensor, temporal_resolution=layer_step.temporal_resolution,
                                maxzoom=22, minzoom=0, bbox=bbox_extent, resolution=Decimal(resolution))
    cfg.db.add_layer_step(layer_step)
