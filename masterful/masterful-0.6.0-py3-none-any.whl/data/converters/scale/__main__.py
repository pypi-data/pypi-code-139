"""Entrypoint for the masterful.data.converters.scale package."""

import argparse
import os

try:
  import scaleapi
except ImportError:
  print(
      "ScaleAI data conversion requires the `scaleapi` Python package to be "
      "installed. Please run `pip install scaleapi` in your current environment and try again."
  )
  exit()

import masterful

# Activate only if not running locally
if 'backend' not in dir(masterful) or os.environ.get('NOOP_REGISTER',
                                                     None) == '1':
  masterful = masterful.activate()

from masterful.data.converters.scale import convert_annotations
from masterful.utils import logging as masterful_logging


def _validate_arguments(args: argparse.Namespace):
  """Check for additional argument compatibility not handled by argparse.

  Args:
    args: Arguments for Scale converter returned by argparse.
  """
  if args.project_name and not (args.scale_api_key_path or
                                "SCALE_API_KEY" in os.environ):
    raise ValueError(
        ("Scale project was defined without setting the Scale API key to "
         "download it."))


def _get_scale_client(scale_api_key_path: str) -> scaleapi.ScaleClient:
  """Instantiates a Scale client with the live API key provided by Scale.

  Args:
    scale_api_key_path: Path to a file containing the key.

  Returns:
    ScaleClient used to download project data from Scale.
  """
  scale_client = None

  if scale_api_key_path:
    with open(scale_api_key_path, "r") as file:
      scale_api_key = file.read().strip()
    scale_client = scaleapi.ScaleClient(scale_api_key)
  elif "SCALE_API_KEY" in os.environ:
    scale_client = scaleapi.ScaleClient(os.environ["SCALE_API_KEY"])

  return scale_client


def main():
  """Main entrypoint for the standalone version of this package."""
  parser = argparse.ArgumentParser(prog="convert_annotations")
  parser._action_groups.pop()
  required_group = parser.add_argument_group("Required Arguments")
  optional_group = parser.add_argument_group("Optional Arguments")

  data_source_group = required_group.add_mutually_exclusive_group(required=True)
  data_source_group.add_argument(
      "-p",
      "--project_name",
      type=str,
      help=("Scale project name to download current data from. The Scale API "
            "key must be set in order to download. Batches can be selected by "
            "setting the optional 'created_after' and 'created_before' "
            "arguments."))
  data_source_group.add_argument(
      "-j",
      "--json_path",
      type=str,
      help="Scale JSON file path. Supports local, AWS, and GCP paths.")

  required_group.add_argument(
      "-t",
      "--task",
      nargs="?",
      choices=[
          "image_classification", "object_detection", "semantic_segmentation"
      ],
      required=True,
      help="Types of computer vision tasks supported by Masterful.")

  required_group.add_argument(
      "-o",
      "--output_path",
      type=str,
      required=True,
      help="Local destination folder to store output files.")

  parser.add_argument(
      "-n",
      "--batch_names",
      nargs="+",
      required=False,
      help=("Names of batches to convert data from. If not defined, all will "
            "be selected."))

  optional_group.add_argument(
      "-a",
      "--created_after",
      type=str,
      required=False,
      help="Only select annotations after specified date (YYYY-MM-DD).")

  optional_group.add_argument(
      "-b",
      "--created_before",
      type=str,
      required=False,
      help="Only select annotations before specified date (YYYY-MM-DD).")

  optional_group.add_argument(
      "-k",
      "--scale_api_key_path",
      type=str,
      required=False,
      help=("Path to file containing the live API key used by Scale for "
            "refreshing download URLs (or set the 'SCALE_API_KEY' environment "
            "variable). If not defined, expired default URLs will be used."))

  optional_group.add_argument(
      "-d",
      "--download_images",
      action="store_true",
      required=False,
      help="Choose whether or not to download image files to output folder.")

  args = parser.parse_args()
  _validate_arguments(args)

  scale_client = _get_scale_client(args.scale_api_key_path)

  logger, _, _ = masterful_logging.create_or_return_logger(
      "masterful.data.converters.scale")

  convert_annotations.write_metadata(project_name=args.project_name,
                                     json_path=args.json_path,
                                     task=args.task,
                                     output_path=args.output_path,
                                     batch_names=args.batch_names,
                                     created_after=args.created_after,
                                     created_before=args.created_before,
                                     scale_client=scale_client,
                                     download_images=args.download_images,
                                     logger=logger)


if __name__ == "__main__":
  main()