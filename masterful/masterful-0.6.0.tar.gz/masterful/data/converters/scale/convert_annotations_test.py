"Unit tests for functions defined within scale/convert_annotations.py."
import json
import logging
import os
import tempfile

from PIL import Image
import numpy as np
import tensorflow as tf

import masterful.data.converters.scale.convert_annotations as convert_annotations


class ConvertAnnotationsTest(tf.test.TestCase):
  """Unit tests for functions defined within scale/convert_annotations.py."""

  def test_is_valid_annotation_valid_when_filters_are_undefined(self):
    annotation = {
        "task_id": "1234abcd",
        "created_at": "2022-02-02T02:22:22.222Z",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
    }

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=None,
        created_after="",
        created_before="",
        logger=logging.getLogger())

    self.assertEqual(result, True)

  def test_is_valid_annotation_invalid_when_not_in_batch(self):
    annotation = {
        "task_id": "1234abcd",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
        "batch": "invalid_batch"
    }
    batch_names = ["valid_batch"]

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=batch_names,
        created_after="",
        created_before="",
        logger=logging.getLogger())

    self.assertEqual(result, False)

  def test_is_valid_annotation_valid_when_in_batch(self):
    annotation = {
        "task_id": "1234abcd",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
        "batch": "valid_batch"
    }
    batch_names = ["valid_batch"]

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=batch_names,
        created_after="",
        created_before="",
        logger=logging.getLogger())

    self.assertEqual(result, True)

  def test_is_valid_annotation_invalid_when_out_of_range_of_created_before(
      self):
    annotation = {
        "task_id": "1234abcd",
        "created_at": "2022-02-02T02:22:22.222Z",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
    }

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=None,
        created_after="",
        created_before="2022-02-01",
        logger=logging.getLogger())

    self.assertEqual(result, False)

  def test_is_valid_annotation_valid_when_created_in_range_of_before_cutoff(
      self):
    annotation = {
        "task_id": "1234abcd",
        "created_at": "2022-02-02T02:22:22.222Z",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
    }

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=None,
        created_after="",
        created_before="2022-02-03",
        logger=logging.getLogger())

    self.assertEqual(result, True)

  def test_is_valid_annotation_invalid_when_out_of_range_of_created_after(self):
    annotation = {
        "task_id": "1234abcd",
        "created_at": "2022-02-02T02:22:22.222Z",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
    }

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=None,
        created_after="2022-02-03",
        created_before="",
        logger=logging.getLogger())

    self.assertEqual(result, False)

  def test_is_valid_annotation_valid_when_in_range_of_created_after(self):
    annotation = {
        "task_id": "1234abcd",
        "created_at": "2022-02-02T02:22:22.222Z",
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        },
    }

    result = convert_annotations._is_valid_annotation(
        ann=annotation,
        batch_names=None,
        created_after="2022-02-01",
        created_before="",
        logger=logging.getLogger())

    self.assertEqual(result, True)

  def test_get_converted_image_location_when_not_downloading(self):
    annotation = {
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "expected_label_url"
        }]
    }
    invalid_output_path = "invalid_path"

    result = convert_annotations._get_converted_image_location(
        ann=annotation, download=False, output_path=invalid_output_path)

    self.assertEqual(result, "expected_label_url")
    self.assertEqual(os.path.exists(invalid_output_path), False)

  def test_get_converted_image_location_when_downloading(self):
    with tempfile.TemporaryDirectory() as temp_dir:
      annotation = {
          "metadata": {
              "filename": "image_01.jpg"
          },
          "attachmentS3Downloads": [{
              "isConvertedImage": True,
              "s3URL": os.path.join(temp_dir, "image_01.jpg")
          }]
      }
      image = Image.fromarray(np.zeros((2, 2, 3), dtype=np.uint8))
      image.save(os.path.join(temp_dir, "image_01.jpg"))

      result = convert_annotations._get_converted_image_location(
          ann=annotation, download=True, output_path=temp_dir)

      self.assertTrue(
          os.path.exists(os.path.join(temp_dir, "images", "image_01.jpg")))
    self.assertEqual(result, os.path.join(temp_dir, "images", "image_01.jpg"))

  def test_get_segmentation_label_location_when_not_downloading(self):
    annotation = {
        "response": {
            "annotations": {
                "combined": {
                    "indexedImage": "expected_label_url"
                }
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
    }
    invalid_output_path = "invalid_path"

    result = convert_annotations._get_segmentation_label_location(
        ann=annotation, download=False, output_path=invalid_output_path)

    self.assertEqual(result, "expected_label_url")
    self.assertEqual(os.path.exists(invalid_output_path), False)

  def test_get_segmentation_label_location_when_downloading(self):
    with tempfile.TemporaryDirectory() as temp_dir:
      annotation = {
          "response": {
              "annotations": {
                  "combined": {
                      "indexedImage": os.path.join(temp_dir, "image_01.jpg")
                  }
              }
          },
          "metadata": {
              "filename": "image_01.jpg"
          },
      }
      image = Image.fromarray(np.zeros((2, 2, 3), dtype=np.uint8))
      image.save(os.path.join(temp_dir, "image_01.jpg"))

      result = convert_annotations._get_segmentation_label_location(
          ann=annotation, download=True, output_path=temp_dir)

      self.assertTrue(
          os.path.exists(os.path.join(temp_dir, "images",
                                      "image_01_label.jpg")))
    self.assertEqual(result,
                     os.path.join(temp_dir, "images", "image_01_label.jpg"))

  def test_get_label_map_with_unsupported_type_raises_valueerror(self):
    annotation = {"type": "unsupported_type"}

    with self.assertRaises(ValueError) as cm:
      _ = convert_annotations._get_label_map(annotation)

    self.assertEqual(
        "Expected 'objects_to_annotate' to be present in imageannotation "
        "or 'labelMapping' to be present in 'segmentannotation'",
        str(cm.exception))

  def test_get_label_map_with_invalid_imageannotation_raises_keyerror(self):
    annotation = {
        "type": "imageannotation",
        "params": {
            "geometries": {
                "point": {}
            }
        }
    }

    with self.assertRaises(KeyError) as cm:
      _ = convert_annotations._get_label_map(annotation)

    self.assertEqual("'objects_to_annotate'", str(cm.exception))

  def test_get_label_map_with_valid_imageannotation(self):
    annotation = {
        "type": "imageannotation",
        "params": {
            "geometries": {
                "box": {
                    "objects_to_annotate": ["label_01"]
                },
                "polygon": {
                    "objects_to_annotate": ["label_02"]
                },
                "point": {
                    "objects_to_annotate": ["label_03"]
                },
                "line": {
                    "objects_to_annotate": ["label_06"]
                },
                "cuboid": {
                    "objects_to_annotate": ["label_05"]
                },
                "ellipse": {
                    "objects_to_annotate": ["label_04"]
                }
            }
        }
    }

    expected = {
        0: "label_01",
        1: "label_02",
        2: "label_03",
        3: "label_04",
        4: "label_05",
        5: "label_06"
    }

    result = convert_annotations._get_label_map(annotation)

    self.assertDictEqual(result, expected)

  def test_get_label_map_with_valid_segmentannotation_for_classification(self):
    annotation = {
        "type": "segmentannotation",
        "response": {
            "labelMapping": {
                "label_after_1": {
                    "index": 2
                },
                "label_before_2": {
                    "index": 1
                }
            }
        }
    }

    expected = {1: "label_before_2", 2: "label_after_1"}

    result = convert_annotations._get_label_map(annotation,
                                                "image_classification")

    self.assertDictEqual(result, expected)

  def test_get_label_map_with_valid_segmentannotation_for_segmentation(self):
    annotation = {
        "type": "segmentannotation",
        "response": {
            "labelMapping": {
                "label_after_1": {
                    "index": 2
                },
                "label_before_2": {
                    "index": 1
                }
            }
        }
    }

    expected = {0: "background", 1: "label_before_2", 2: "label_after_1"}

    result = convert_annotations._get_label_map(annotation,
                                                "semantic_segmentation")

    self.assertDictEqual(result, expected)

  def test_parse_json_file_for_imageannotation_image_classification(self):
    annotation_list = [{
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02"
            }]
        }
    }, {
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "point": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_02.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_02_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_01"
            }, {
                "label": "label_02"
            }]
        }
    }]

    expected = ([["image_01_url", 1], ["image_02_url", 0, 1]], {
        0: "label_01",
        1: "label_02"
    })

    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
      json.dump(annotation_list, temp_file)
      temp_file.flush()

      result = convert_annotations._parse_json_file(json_path=temp_file.name,
                                                    task="image_classification",
                                                    batch_names=None,
                                                    created_after="",
                                                    created_before="",
                                                    logger=logging.getLogger())

    self.assertEqual(result, expected)

  def test_parse_json_file_for_imageannotation_object_detection(self):
    annotation_list = [{
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "box": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_01.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_02",
                "left": 1.01,
                "top": 2.99,
                "height": 3,
                "width": 6,
                "type": "box"
            }]
        }
    }, {
        "type": "imageannotation",
        "status": "completed",
        "params": {
            "geometries": {
                "box": {
                    "objects_to_annotate": ["label_01", "label_02"]
                },
            }
        },
        "metadata": {
            "filename": "image_02.jpg"
        },
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_02_url"
        }],
        "response": {
            "annotations": [{
                "label": "label_01",
                "left": 1.0,
                "top": 1.0,
                "height": 1.0,
                "width": 1.0,
                "type": "box"
            }, {
                "label": "label_02",
                "left": 1.0,
                "top": 1.0,
                "height": 1.0,
                "width": 1.0,
                "type": "box"
            }]
        }
    }]

    expected = ([["image_01_url", 1, 2, 1, 5, 7],
                 ["image_02_url", 0, 1, 1, 2, 2, 1, 1, 1, 2, 2]], {
                     0: "label_01",
                     1: "label_02"
                 })

    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
      json.dump(annotation_list, temp_file)
      temp_file.flush()

      result = convert_annotations._parse_json_file(json_path=temp_file.name,
                                                    task="object_detection",
                                                    batch_names=None,
                                                    created_after="",
                                                    created_before="",
                                                    logger=logging.getLogger())

    self.assertEqual(result, expected)

  def test_parse_json_file_for_segmentannotation_image_classification(self):
    annotation_list = [{
        "type": "segmentannotation",
        "status": "completed",
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "labelMapping": {
                "label_01": {
                    "index": 1,
                    "numPixels": 0
                },
                "label_02": {
                    "index": 2,
                    "numPixels": 1000
                }
            }
        }
    }, {
        "type": "segmentannotation",
        "status": "completed",
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_02_url"
        }],
        "response": {
            "labelMapping": {
                "label_01": {
                    "index": 1,
                    "numPixels": 1
                },
                "label_02": {
                    "index": 2,
                    "numPixels": 1000
                }
            }
        }
    }]

    expected = ([["image_01_url", 2], ["image_02_url", 1, 2]], {
        1: "label_01",
        2: "label_02"
    })

    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
      json.dump(annotation_list, temp_file)
      temp_file.flush()

      result = convert_annotations._parse_json_file(json_path=temp_file.name,
                                                    task="image_classification",
                                                    batch_names=None,
                                                    created_after="",
                                                    created_before="",
                                                    logger=logging.getLogger())

    self.assertEqual(result, expected)

  def test_parse_json_file_for_segmentannotation_semantic_segmentation(self):
    annotation_list = [{
        "type": "segmentannotation",
        "status": "completed",
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_01_url"
        }],
        "response": {
            "annotations": {
                "combined": {
                    "indexedImage": "image_01_label_url"
                }
            },
            "labelMapping": {
                "label_01": {
                    "index": 1,
                    "numPixels": 0
                },
                "label_02": {
                    "index": 2,
                    "numPixels": 1000
                }
            }
        }
    }, {
        "type": "segmentannotation",
        "status": "completed",
        "attachmentS3Downloads": [{
            "isConvertedImage": True,
            "s3URL": "image_02_url"
        }],
        "response": {
            "annotations": {
                "combined": {
                    "indexedImage": "image_02_label_url"
                }
            },
            "labelMapping": {
                "label_01": {
                    "index": 1,
                    "numPixels": 1
                },
                "label_02": {
                    "index": 2,
                    "numPixels": 1000
                }
            }
        }
    }]

    expected = ([["image_01_url", "image_01_label_url"],
                 ["image_02_url", "image_02_label_url"]], {
                     0: "background",
                     1: "label_01",
                     2: "label_02"
                 })

    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
      json.dump(annotation_list, temp_file)
      temp_file.flush()

      result = convert_annotations._parse_json_file(
          json_path=temp_file.name,
          task="semantic_segmentation",
          batch_names=None,
          created_after="",
          created_before="",
          logger=logging.getLogger())

    self.assertEqual(result, expected)


if __name__ == "__main__":
  tf.test.main()