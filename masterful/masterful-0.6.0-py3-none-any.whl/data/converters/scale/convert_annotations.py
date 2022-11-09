"""Scale data format converter for the Masterful CLI trainer."""

import json
import logging
import os
from datetime import datetime
from typing import List, Tuple, Union

try:
  import scaleapi
except ImportError:
  print(
      "ScaleAI data conversion requires the `scaleapi` Python package to be "
      "installed. Please run `pip install scaleapi` in your current environment and try again."
  )
  exit()

import smart_open
from PIL import Image
from scaleapi.tasks import TaskStatus


def _is_valid_annotation(ann: dict, batch_names: List[str], created_after: str,
                         created_before: str, logger: logging.Logger) -> bool:
  """Helper function that determines which annotations qualify for use."""
  is_valid = True
  if (isinstance(batch_names, list) and len(batch_names) > 0 and
      ann["batch"] not in batch_names):
    logger.info(f"Skipping {ann['task_id']}. Filtering out batch "
                "{ann['batch']}.")
    is_valid = False

  if not (not created_before or
          (created_before and
           datetime.strptime(ann["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ") <
           datetime.strptime(created_before, "%Y-%m-%d"))):
    logger.info(f"Skipping {ann['task_id']}. Created after {created_before}.")
    is_valid = False

  if not (not created_after or
          (created_after and
           datetime.strptime(ann["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ") >
           datetime.strptime(created_after, "%Y-%m-%d"))):
    logger.info(f"Skipping {ann['task_id']}. Created before {created_after}.")
    is_valid = False

  return is_valid


def _get_label_map(annotation: Union[dict, scaleapi.tasks.Task],
                   task: str = "") -> dict:
  """Builds a label map from a Scale image or segment annotation.

  Args:
    annotation: A scale annotation dictionary.

  Returns:
    A label map dictionary. Example format: {0: cat, 1: dog}
  """
  if isinstance(annotation, scaleapi.tasks.Task):
    annotation = annotation.as_dict()

  label_map = {}
  label_set = set()

  if annotation["type"] == "imageannotation":
    if "box" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["box"]["objects_to_annotate"])

    if "polygon" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["polygon"]["objects_to_annotate"])

    if "point" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["point"]["objects_to_annotate"])

    if "line" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["line"]["objects_to_annotate"])

    if "cuboid" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["cuboid"]["objects_to_annotate"])

    if "ellipse" in annotation["params"]["geometries"].keys():
      label_set.update(
          annotation["params"]["geometries"]["ellipse"]["objects_to_annotate"])

    label_map.update(enumerate(sorted(label_set)))

  elif annotation["type"] == "segmentannotation":
    label_map = {0: "background"} if task == "semantic_segmentation" else {}
    label_map = {
        **label_map,
        **{
            value["index"]: key for key, value in annotation["response"]["labelMapping"].items(
            )
        }
    }

  if len(label_map) == 0:
    raise ValueError(
        "Expected 'objects_to_annotate' to be present in imageannotation "
        "or 'labelMapping' to be present in 'segmentannotation'")

  return label_map


def _get_converted_image_location(ann: dict,
                                  download: bool = False,
                                  output_path: str = "") -> str:
  """Returns converted image URL or path of downloaded image."""
  for attachment in ann["attachmentS3Downloads"]:
    if attachment["isConvertedImage"]:
      if download:
        os.makedirs(os.path.join(output_path, "images"), exist_ok=True)
        with smart_open.open(attachment["s3URL"], "rb") as file:
          image = Image.open(file)
          filename = ann["metadata"]["filename"]
          image.save(os.path.join(output_path, "images", filename))
        return os.path.join(output_path, "images", filename)
      return attachment["s3URL"]


def _get_segmentation_label_location(ann: dict,
                                     download: bool = False,
                                     output_path: str = "") -> str:
  """Returns segmentation label URL or path of downloaded image."""
  label_url = ann["response"]["annotations"]["combined"]["indexedImage"]
  if download:
    os.makedirs(os.path.join(output_path, "images"), exist_ok=True)
    with smart_open.open(label_url, "rb") as file:
      image = Image.open(file)
      file_name, file_extension = os.path.splitext(ann["metadata"]["filename"])
      label_path = os.path.join(output_path, "images",
                                file_name + "_label" + file_extension)
      image.save(label_path)
    return label_path
  return label_url


def _get_updated_imageannotation_records(records: List[List[str]], ann: dict,
                                         task: str, label_map: dict,
                                         download: bool, output_path: str,
                                         logger: logging.Logger):
  """Appends a new record with data parsed from an imageannotation sample."""
  if download:
    record = [
        _get_converted_image_location(ann=ann,
                                      download=download,
                                      output_path=output_path)
    ]
  else:
    for attachment in ann["attachmentS3Downloads"]:
      if attachment["isConvertedImage"]:
        record = [attachment["s3URL"]]

  for response_annotation in ann["response"]["annotations"]:
    if task == "image_classification":
      record.append(
          list(label_map.keys())[list(label_map.values()).index(
              response_annotation["label"])])
    elif task == "object_detection":
      record.append(
          list(label_map.keys())[list(label_map.values()).index(
              response_annotation["label"])])
      record.extend([
          int(response_annotation["top"]),  # ymin
          int(response_annotation["left"]),  # xmin
          int(response_annotation["top"]) +
          int(response_annotation["height"]),  # ymax
          int(response_annotation["left"]) +
          int(response_annotation["width"]),  # xmax
      ])
    else:
      logger.warning(
          f"Skipping task_id {ann['task_id']}. Only image classification "
          "and object detection are supported for Scale's image "
          "annotation.")
      return records

  records.append(record)
  return records


def _get_updated_segmentannotation_records(records: List[List[str]], ann: dict,
                                           task: str, label_map: dict,
                                           download: bool, output_path: str,
                                           logger: logging.Logger):
  """Appends a new record with data parsed from a segmentannotation sample."""

  record = [
      _get_converted_image_location(ann=ann,
                                    download=download,
                                    output_path=output_path)
  ]

  if task == "image_classification":
    for label, mapping in ann["response"]["labelMapping"].items():
      if mapping["numPixels"] > 0:
        record.append(
            list(label_map.keys())[list(label_map.values()).index(label)])
  elif task == "semantic_segmentation":
    record.append(
        _get_segmentation_label_location(ann=ann,
                                         download=download,
                                         output_path=output_path))
  else:
    logger.warning(
        f"Skipping task_id {ann['task_id']}. Only image classification and "
        "semantic segmentation are supported for Scale's segment "
        "annotations.")
    return records

  records.append(record)
  return records


def _parse_project_annotations(project_name: str, task: str, output_path: str,
                               batch_names: List[str], created_after: str,
                               created_before: str,
                               scale_client: scaleapi.ScaleClient,
                               download_images: bool,
                               logger: logging.Logger) -> Tuple[List, dict]:
  """Download project data from Scale and parse the data according to task."""
  records = []
  label_map = None

  annotations = scale_client.get_tasks(project_name=project_name,
                                       created_after=created_after,
                                       completed_before=created_before,
                                       status=TaskStatus.Completed)

  for ann in annotations:
    ann = scale_client.get_task(ann.task_id).as_dict()

    if not _is_valid_annotation(ann=ann,
                                batch_names=batch_names,
                                created_after=created_after,
                                created_before=created_before,
                                logger=logger):
      continue

    if label_map is None:
      label_map = _get_label_map(ann, task)

    if ann["type"] == "imageannotation" and ann["status"] == "completed":
      records = _get_updated_imageannotation_records(records, ann, task,
                                                     label_map, download_images,
                                                     output_path, logger)
    elif ann["type"] == "segmentannotation" and ann["status"] == "completed":
      records = _get_updated_segmentannotation_records(records, ann, task,
                                                       label_map,
                                                       download_images,
                                                       output_path, logger)
    else:
      logger.warning(
          f"Skipping task_id: '{ann['task_id']}'. Valid image and segment "
          "annotations must be completed.")

  return records, label_map


def _read_json_file(json_path: str) -> List:
  """Read JSON file regardless if stored locally, AWS, or GCP."""
  with smart_open.open(json_path, "r") as json_file:
    annotation_list = json.load(json_file)

  return annotation_list


def _parse_json_file(json_path: str, task: str, batch_names: List[str],
                     created_after: str, created_before: str,
                     logger: logging.Logger) -> Tuple[List, dict]:
  """Parse data from Scale JSON file according to task."""
  records = []
  label_map = None
  annotation_list = _read_json_file(json_path)

  for ann in annotation_list:
    if not _is_valid_annotation(ann=ann,
                                batch_names=batch_names,
                                created_after=created_after,
                                created_before=created_before,
                                logger=logger):
      continue

    if label_map is None:
      label_map = _get_label_map(ann, task)

    if ann["type"] == "imageannotation" and ann["status"] == "completed":
      records = _get_updated_imageannotation_records(records, ann, task,
                                                     label_map, False, "",
                                                     logger)
    elif ann["type"] == "segmentannotation" and ann["status"] == "completed":
      records = _get_updated_segmentannotation_records(records, ann, task,
                                                       label_map, False, "",
                                                       logger)
    else:
      logger.warning(
          f"Skipping task_id: '{ann['task_id']}'. Valid image and segment "
          "annotations must be completed.")

  return records, label_map


def write_metadata(project_name: str, json_path: str, task: str,
                   output_path: str, batch_names: List[str], created_after: str,
                   created_before: str, scale_client: scaleapi.ScaleClient,
                   download_images: bool, logger: logging.Logger):
  """Converts Scale output and writes it to label_map.csv and records.csv

  Args:
    project_name: Scale project name to download current data from.
    json_path: Scale JSON file path. Supports local, AWS, and GCP paths.
    task: String that determines how annotations are parsed
          (image_classification, object_detection, semantic_segmentation)
    output_path: Local path where Masterful metadata files will be written.
    batch_names: Names of batches to convert data from. If not defined, all
                 be selected.
    created_after: Only select annotations after specified date (YYYY-MM-DD).
    created_before: Only select annotations before specified date (YYYY-MM-DD).
    scale_client: ScaleClient used to download project data from Scale.
    download_images: Choose whether or not to download images to output folder.
    logger: Logger for reporting progress of data conversion.
  """
  if project_name and not json_path:
    records, label_map = _parse_project_annotations(
        project_name, task, output_path, batch_names, created_after,
        created_before, scale_client, download_images, logger)
  elif json_path and not project_name:
    records, label_map = _parse_json_file(json_path, task, batch_names,
                                          created_after, created_before, logger)
  else:
    raise Exception("Select one data source: project_name or json_path.")

  with open(os.path.join(output_path, "label_map.csv"), "w") as fp:
    for index, label in label_map.items():
      fp.write(f"{str(index)}, {label}\n")

  with open(os.path.join(output_path, "records.csv"), "w") as fp:
    for i, record in enumerate(records):
      if i != len(records) - 1:
        fp.write(", ".join(str(e) for e in record) + os.linesep)
      else:
        fp.write(", ".join(str(e) for e in record))