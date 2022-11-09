"""Entrypoint for the masterful.evaluate package.

Evaluates the trained model based on the training configuration file.
"""
import os
# Must be set before importing tensorflow.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_CPP_MAX_LOG_LEVEL'] = '0'
os.environ['TF_CPP_MAX_VLOG_LEVEL'] = '0'

import argparse
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu, True)

import dataclasses
import io
import smart_open
from tabulate import tabulate
from tqdm import tqdm
import yaml

# Register if not running locally. Registration
# only works by using the evironment variables.
import masterful
if 'backend' not in dir(masterful) or os.environ.get('NOOP_REGISTER',
                                                     None) == '1':
  masterful = masterful.activate()

from masterful.data import analyzer
import masterful.train.data as data_loader
import masterful.train.evaluation as training_evaluation
import masterful.train.output as output
import masterful.train.preprocessing as preprocessor
import masterful.train.validation as validator
import masterful.utils.logging as masterful_logging
import masterful.utils.dataset as dataset_utils
import masterful.utils.model as model_utils


def _silence_logging():
  tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

  import logging

  logging.getLogger('tensorflow').setLevel(logging.ERROR)
  logging.getLogger('absl').setLevel(logging.ERROR)
  logging.getLogger().setLevel(logging.ERROR)

  from absl import logging as absl_logging
  absl_logging.set_verbosity(absl_logging.ERROR)


_silence_logging()


def evaluate(
    config_path: str,
    saved_model_path: str,
    num_examples: int = -1,
    print_misclassifications: bool = False,
):
  logger, _, _ = masterful_logging.create_or_return_logger('masterful.evaluate')

  # Set the detection backend to internal so that we
  # don't use the installed OD API packages
  model_utils.set_detection_backend(True)

  # Parse the YAML configuration file
  logger.console(f"Evaluating with configuration '{config_path}':")
  try:
    with smart_open.open(config_path, "r") as yaml_file:
      config_str = yaml_file.read()
      config = yaml.safe_load(io.StringIO(config_str))
  except:
    logger.console(
        f"Unable to open configuration file '{config_path}'. Please ensure this path/file exists and is accessible."
    )
    masterful_logging.log_trainer_event(None)
    return
  masterful_logging.log_trainer_event(config_str)

  # Print out the training configuration parameters
  analyzer.print_analysis_results(config)

  # Basic section checking upfront
  validator.check_for_required_configuration(config)
  validator.warn_on_improper_configuration(config)

  # Load the model architecture
  input_shape = tuple(config['model']['input_shape'])
  num_classes = config['model']['num_classes']

  task_desc = config["training"]["task"]
  if task_desc == "binary_classification":
    if num_classes != 1:
      raise ValueError(
          f"Task is 'binary_classification' but num_classes {num_classes} != 1."
      )
    task = masterful.enums.Task.BINARY_CLASSIFICATION
    sparse = True
  elif task_desc == "classification":
    if num_classes <= 1:
      raise ValueError(
          f"Task is 'classification' but num_classes {num_classes} <= 1.")
    task = masterful.enums.Task.CLASSIFICATION
    sparse = False
  elif task_desc == "multilabel_classification":
    if num_classes <= 1:
      raise ValueError(
          f"Task is 'multilabel_classification' but num_classes {num_classes} <= 1."
      )
    task = masterful.enums.Task.MULTILABEL_CLASSIFICATION
    sparse = False
  elif task_desc == "detection":
    if num_classes < 1:
      raise ValueError(
          f"Task is 'detection' but num_classes {num_classes} < 1.")
    task = masterful.enums.Task.DETECTION
    sparse = False
  elif task_desc == "semantic_segmentation":
    task = masterful.enums.Task.SEMANTIC_SEGMENTATION
    sparse = False
  else:
    raise ValueError(f"Unknown task {task_desc}.")

  architecture = config['model']['architecture']
  logger.console(F"Building model '{architecture}'...")
  model, (preprocessing, model_image_range,
          model_config) = masterful.architecture.load_model(
              architecture=architecture,
              task=task,
              input_shape=input_shape,
              num_classes=num_classes)

  logger.console("Loading evaluation dataset.")
  splits = data_loader.load_splits_from_config(config, num_classes, task,
                                               logger)

  test_dataset = None
  test_dataset_split_name = None
  if "evaluation" in config:
    if "split" in config['evaluation']:
      if config['evaluation']['split'] in splits:
        test_dataset_split_name = config['evaluation']['split']
        test_dataset = splits[test_dataset_split_name]
      else:
        raise ValueError(
            f"Test split {config['evaluation']['split']} not found in datasets section."
        )

  if test_dataset is None:
    logger.console(
        "No test dataset specified in configuration file. Nothing to evaluate.")
    return

  # Preprocess the data.
  test_dataset_cardinality = dataset_utils.cardinality(test_dataset)
  dataset_preprocessing = preprocessor.preprocess(input_shape, num_classes,
                                                  preprocessing, task)
  test_dataset = test_dataset.map(dataset_preprocessing, tf.data.AUTOTUNE)
  test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)
  setattr(test_dataset, '_masterful_cardinality', test_dataset_cardinality)

  if model_utils.is_tensorflow_object_detection_model(model):
    model_params = masterful.architecture.ArchitectureParams(
        task=masterful.enums.Task.DETECTION,
        input_range=masterful.enums.ImageRange.ZERO_255,
        input_shape=input_shape,
        input_dtype=tf.float32,
        num_classes=num_classes,
        prediction_dtype=tf.float32,
        prediction_structure=masterful.enums.TensorStructure.DICT,
        prediction_logits=True,
        prediction_shape=None,
        model_config=model_config,
    )
  else:
    model_params = masterful.architecture.learn_architecture_params(
        model,
        task,
        input_range=model_image_range,
        num_classes=num_classes,
        prediction_logits=True)

  bounding_box_format = masterful.enums.BoundingBoxFormat.TENSORFLOW if model_utils.is_tensorflow_object_detection_model(
      model) else None
  test_dataset_params = masterful.data.learn_data_params(
      test_dataset,
      model_image_range,
      num_classes,
      sparse,
      task,
      bounding_box_format=bounding_box_format)

  # Create the inference model from the saved model path
  inference_model_preprocessing = preprocessor.preprocess(
      input_shape, 0, preprocessing, task, True)

  if model_utils.is_tensorflow_object_detection_model(model):
    from masterful.architecture.detection import model as object_detection_model_utils
    training_model = object_detection_model_utils.TFObjectDetectionTrainingModel(
        model, batch_size=1)

    # In order to use the wrapped model, we need to make sure the
    # weights have been loaded. So let's predict on a dummy batch.
    training_model.ensure_weights(input_shape=(
        model_params.input_height,
        model_params.input_width,
        model_params.input_channels,
    ),
                                  label_shape=test_dataset_params.label_shape)

    training_model.build(
        (1, model_params.input_height, model_params.input_width,
         model_params.input_channels))

    inference_model = output.create_inference_model(
        model,
        model_params,
        inference_model_preprocessing,
    )
  else:
    training_model = model

    inference_model = output.create_inference_model(
        training_model,
        model_params,
        inference_model_preprocessing,
    )

  # Load the weights into the training model from the
  # saved inference model.
  logger.console("Loading saved model weights for evaluation.")
  inference_model.load_weights(saved_model_path)
  training_model.set_weights(inference_model.get_weights())

  optimization_params = masterful.optimization.learn_optimization_params(
      training_model,
      model_params,
      test_dataset,
      test_dataset_params,
      batch_size=1,
      _disable_progress=True,
      _disable_dataset_validation=True,
  )
  logger.console("Evaluating model with optimization parameters:")
  print(tabulate(dataclasses.asdict(optimization_params).items()))
  training_model.compile(loss=optimization_params.loss,
                         metrics=optimization_params.metrics)

  if num_examples > 0:
    test_dataset = test_dataset.take(num_examples)
    test_dataset_cardinality = num_examples

  _ = training_evaluation.evaluate(
      training_model,
      model_params,
      test_dataset,
      test_dataset_params,
      1,
      task == masterful.enums.Task.DETECTION,  # drop_remainder
      test_dataset_split_name,
      config,
      logger,
      detection_model=model,  # Detection only
      verbose=1,
  )

  if print_misclassifications:
    _print_misclassifications(
        inference_model,
        model_params,
        config,
        test_dataset_cardinality,
        logger,
    )


def _print_misclassifications(
    inference_model,
    model_params,
    config,
    num_examples,
    logger,
):
  if model_params.task != masterful.enums.Task.BINARY_CLASSIFICATION:
    logger.console(
        "Mis-classifications only supported for binary classification.")
    return

  if not 'dataset' in config:
    raise ValueError("Configuration file contains no 'dataset' section.")
  dataset_spec = config['dataset']

  if not 'root_path' in dataset_spec:
    raise ValueError(
        "'root_path' is not specified in 'dataset' section. Please specify the root path to your dataset."
    )
  dataset_root = dataset_spec['root_path']

  test_csv_path = None
  if "evaluation" in config:
    if "split" in config['evaluation']:
      split_name = config['evaluation']['split']
      test_csv_path = os.path.join(dataset_root, f"{split_name}.csv")

  image_paths = []
  num_paths = 0
  logger.console("Calculating mis-classifications.")
  with smart_open.open(test_csv_path, "r") as fp:
    lines = fp.readlines()
    for line in lines:
      if num_paths > num_examples:
        break

      # Split the line based on ',' character.
      # First entry is the full path to the image to
      # be loaded, the rest of the entrees are the labels
      # for that image.
      line = line.strip()
      if not line:
        continue

      num_paths += 1
      tokens = line.split(',')
      image_path = None
      if dataset_root is not None:
        image_path = os.path.join(dataset_root, tokens[0].strip())
      else:
        image_path = tokens[0].strip()

      image_labels = []
      for class_str in tokens[1:]:
        class_str = class_str.strip()
        if class_str:
          image_labels.append(int(class_str))
      image_paths.append((image_path, image_labels))

  false_positives = []
  false_negatives = []
  true_positives = []
  for image_path, image_labels in tqdm(image_paths, desc="Mis-classifications"):
    with smart_open.open(image_path, 'rb') as fp:
      encoded_image = fp.read()
      image = tf.image.decode_image(encoded_image,
                                    channels=3,
                                    expand_animations=False)
      image_label = image_labels[0]
    prediction = inference_model(image)
    prediction = tf.nn.sigmoid(prediction)
    predicted_label = 1 if prediction[0] >= 0.5 else 0
    if image_label == 1 and predicted_label == 0:
      false_negatives.append((image_path, prediction[0][0]))
    if image_label == 0 and predicted_label == 1:
      false_positives.append((image_path, prediction[0][0]))
    if image_label == 1 and predicted_label == 1:
      true_positives.append((image_path, prediction[0][0]))

  logger.console("True Positives:")
  for image_path, score in true_positives:
    logger.console(f"    {image_path}: {score}")

  logger.console("False Positives:")
  for image_path, score in false_positives:
    logger.console(f"    {image_path}: {score}")

  logger.console("False Negatives:")
  for image_path, score in false_negatives:
    logger.console(f"    {image_path}: {score}")


def main(override=None):
  """
  Main entrypoint for the standalone version of this package.
  """
  # This script only runs under Tensorflow 2.0
  assert tf.__version__.startswith("2")

  parser = argparse.ArgumentParser()
  parser.add_argument("--config",
                      help="Training configuration YAML file",
                      type=str,
                      required=True)
  parser.add_argument(
      "--saved_model",
      help="The directory to the saved model output from the trainer.",
      type=str,
      required=True)
  parser.add_argument(
      "--num_examples",
      help=
      "Number of examples to evaluate on. Default is -1, which is all examples.",
      type=int,
      default=-1,
  )
  parser.add_argument(
      "--print_misclassifications",
      help="Print the mis-classifications.",
      action="store_true",
  )

  args = parser.parse_args()

  import warnings
  with warnings.catch_warnings():
    if masterful.constants.MASTERFUL_VERBOSITY < 1:
      warnings.simplefilter("ignore")
    evaluate(config_path=args.config,
             saved_model_path=args.saved_model,
             num_examples=args.num_examples,
             print_misclassifications=args.print_misclassifications)
  sys.exit(0)


main()