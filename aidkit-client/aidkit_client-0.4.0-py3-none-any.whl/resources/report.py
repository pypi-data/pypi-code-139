"""
Resource for the Report 2.0.
"""
import json
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

import altair as alt
import numpy as np
import PIL.Image
from ipywidgets import widgets
from pandas import DataFrame

from aidkit_client._endpoints.models import (
    ClassificationModelOutput,
    ImageObjectDetectionModelOutput,
    ImageSegmentationModelOutput,
    ModelNormStats,
    OutputType,
    ReportAdversarialResponse,
    ReportCoreMethodOutputDetailResponse,
    ReportCorruptionResponse,
    ReportRequest,
)
from aidkit_client._endpoints.report import ReportAPI
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.plotting.base_objects import (
    display_class_color,
    display_inference_per_class_widget,
    display_object_detection_box_count_widget,
    display_observation,
    display_selection_class_detection_widget,
    display_semantic_segmentation_inference_argmax_widget,
    display_static_observation_difference,
    display_table,
    get_inference_argmax_prediction,
    get_inference_per_class_confidence,
)
from aidkit_client.resources.data_point import DataPointType, RemoteFile
from aidkit_client.resources.dataset import Dataset, Observation, Subset
from aidkit_client.resources.ml_model import MLModelVersion


@dataclass
class ModelComparisonView:
    """
    Model-comparison view of the report.
    """

    plot: alt.LayerChart
    stats: DataFrame


@dataclass
class AttackDetailView:
    """
    Attack-detail view of the report.
    """

    plot: alt.LayerChart


@dataclass
class AttackComparisonView:
    """
    Attack-comparison view of the report.
    """

    plot: alt.LayerChart
    stats: Dict[str, DataFrame]


class _BaseReport:
    """
    Base class for the corruption- and the adversarial report.
    """

    _data: Union[ReportCorruptionResponse, ReportAdversarialResponse]

    @property
    def data(self) -> DataFrame:
        """
        Get the data of the report.

        :return: DataFrame containing sample data for the report. The returned DataFrame has one row
            per combination of

            * Configured Method: All those perturbation methods which were run on all compared model
                versions and evaluated with all considered norms are included.
            * Observation: Observation: All observations in the subset the report is requested for.
            * Model Version: All model versions the report is requested for.
            * Metric Name: All norms the report is requested for.

            The returned DataFrame has the following columns:

            * ``successful``: Boolean; Whether the generated perturbation changed the model's
                prediction.
            * ``distance_metric_value``: Float; Distance between the perturbation and the original
                observation.
            * ``method_name``: Categorical; Name of the method used to create the perturbation.
            * ``param_string`` Categorical; Parameters for the method used to create the
                perturbation.
            * ``observation_id``: Integer; ID of the original observation the perturbation was
                created for.
            * ``artifact_id``: Integer; ID of the generated perturbation.
            * ``distance_metric_name``: Categorical; Name of the metric used to measure
                ``distance_metric_value``.
                One of the names in ``metric_names``.
            * ```model_version``: Categorical; Name of the model version the adversarial example was
                created for.
                One of the names in ``model_version_names``.
            * ```perturbation_type``: Categorical; Type of the perturbation, i.e.: 'Corruption'.
        """
        return DataFrame(self._data.data).astype(
            {
                "model_version": "category",
                "distance_metric_name": "category",
                "method_name": "category",
                "param_string": "category",
                "success_metric_type": "category",
                "target_class": "category",
                "perturbation_type": "category",
            }
        )

    def _fill_plot_with_data(self, plot: alt.LayerChart) -> alt.LayerChart:
        plot_copy = plot.copy(deep=True)
        plot_copy.data = self.data
        return plot_copy


class CorruptionReport(_BaseReport):
    """
    A report which compares model versions.
    """

    _data: ReportCorruptionResponse

    def __init__(self, api_service: HTTPService, report_response: ReportCorruptionResponse) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param report_response: Server response describing the report
            to be created.
        """
        self._data = report_response
        self._api_service = api_service
        self.model = ""

    @classmethod
    async def get(
        cls,
        model_name: str,
        model_versions: List[Union[str, MLModelVersion]],
        dataset: Union[str, Dataset],
        subset: Union[str, Subset],
        metrics: List[str],
        success_metric_threshold: float = 0.7,
    ) -> "CorruptionReport":
        """
        Get the adversarial report to compare the given model versions.

        :param model_name: Name of the uploaded model of which versions are compared in the report.
        :param model_versions: List of model versions to compare in the report.
        :param dataset: Dataset to use for the comparison.
        :param subset: Subset whose observations are used for the comparison.
        :param metrics: List of distance metrics to consider in the comparison.
        :param success_metric_threshold: Threshold used to convert
                                        a success metric score to a binary success criterion.
        :return: Instance of the corruption report.
        """
        model_version_names = [
            model_version.name if isinstance(model_version, MLModelVersion) else model_version
            for model_version in model_versions
        ]
        dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
        subset_name = subset.name if isinstance(subset, Subset) else subset
        api_service = get_api_client()
        report = CorruptionReport(
            api_service=api_service,
            report_response=await ReportAPI(api_service).get_corruption_report(
                request=ReportRequest(
                    model=model_name,
                    model_versions=model_version_names,
                    dataset=dataset_name,
                    subset=subset_name,
                    metrics=metrics,
                    success_metric_threshold=success_metric_threshold,
                )
            ),
        )
        report.model = model_name
        return report

    @property
    def model_comparison_plot(self) -> alt.LayerChart:
        """
        Get the model-comparison altair plot.

        :return: Altair plot comparing the corruption robustness of the model
            versions.
        """
        return self._fill_plot_with_data(
            alt.LayerChart.from_dict(self._data.plot_recipes.model_comparison_mfr)
        )


class AdversarialExampleDetails:
    """
    Inference results from the report detailed view corresponding to an
    adversarial example.
    """

    def __init__(
        self,
        api_service: HTTPService,
        adversarial_example_details: ReportCoreMethodOutputDetailResponse,
    ) -> None:
        """
        Create a new instance from the server detailed response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param adversarial_example_details: Server response describing the inference results
            corresponding to a given adversarial example.
        """
        self._api_service = api_service
        self._data = adversarial_example_details

    @classmethod
    async def get_by_adversarial_example_id(
        cls, adversarial_example_id: int
    ) -> "AdversarialExampleDetails":
        """
        Get detailed information on an adversarial example.

        Information consists of:

        * Underlying observation*
        * Inference result of observation*
        * Inference result of adversarial example*
        * Functionality to load adversarial as remote file*

        :param adversarial_example_id: ID of the adversarial example.
        :return: Instance of AdversarialExampleDetails.
        """
        api_service = get_api_client()
        return AdversarialExampleDetails(
            api_service=api_service,
            adversarial_example_details=await ReportAPI(
                api_service
            ).get_adversarial_example_details(adversarial_example_id=adversarial_example_id),
        )

    @property
    def observation_id(self) -> int:
        """
        Get the ID of the original observation from which this adversarial
        example was generated.

        :return: ID of the underlying observation.
        """
        return self._data.observation_id

    @property
    async def observation(self) -> Observation:
        """
        Get the original observation from which this adversarial example was
        generated.

        :return: Instance of the underlying observation.
        """
        return await Observation.get_by_id(self.observation_id)

    @property
    def observation_inference_result(
        self,
    ) -> Union[
        ClassificationModelOutput, ImageSegmentationModelOutput, ImageObjectDetectionModelOutput
    ]:
        """
        Get the underlying observation inference results.

        :return: Instance containing the observation inference results.
        """
        return self._data.observation_inference_result

    @property
    def adversarial_example_id(self) -> int:
        """
        Get the ID of the adversarial example.

        :return: ID of the adversarial example.
        """
        return self._data.core_method_output_id

    def adversarial_example_as_remote_file(self) -> RemoteFile:
        """
        Get an adversarial example as a RemoteFile object.

        :raises ValueError: if method output type is unknown
        :return: remote file
        """
        if self._data.core_method_output_type in ["COLOR_IMAGE", "GREY_SCALE_IMAGE"]:
            data_type = DataPointType.IMAGE
        elif "TEXT" == self._data.core_method_output_type:
            data_type = DataPointType.TEXT
        else:
            raise ValueError(
                f"Unknown type for method output: '{self._data.core_method_output_type}'."
            )
        return RemoteFile(url=self._data.core_method_output_storage_url, type=data_type)

    @property
    def adversarial_example_inference_result(
        self,
    ) -> Union[
        ClassificationModelOutput, ImageSegmentationModelOutput, ImageObjectDetectionModelOutput
    ]:
        """
        Get the adversarial example inference results, i.e.: the softmax output
        of the model.

        :return: Instance containing the adversarial example inference results.
        """
        return self._data.core_method_output_inference_result

    @property
    def inference_class_names(self) -> List[str]:
        """
        Class names for the classes in the inference result.

        :return: List of  class names.
        """
        return self._data.core_method_output_inference_result.class_names


class AdversarialReport(_BaseReport):
    """
    A report which compares model versions.
    """

    _data: ReportAdversarialResponse

    def __init__(
        self, api_service: HTTPService, report_response: ReportAdversarialResponse
    ) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param report_response: Server response describing the report
            to be created.
        """
        self._data = report_response
        self._api_service = api_service
        self.model = ""

    @classmethod
    async def get(
        cls,
        model_name: str,
        model_versions: List[Union[str, MLModelVersion]],
        dataset: Union[str, Dataset],
        subset: Union[str, Subset],
        metrics: List[str],
        success_metric_threshold: float = 0.7,
    ) -> "AdversarialReport":
        """
        Get the adversarial report to compare the given model versions.

        :param model_name: Name of the uploaded model of which versions are compared in the report.
        :param model_versions: List of model versions to compare in the report.
        :param dataset: Dataset to use for the comparison.
        :param subset: Subset whose observations are used for the comparison.
        :param metrics: List of distance metrics to consider in the comparison.
        :param success_metric_threshold: Threshold used to convert
                                        a success metric score to a binary success criterion.
        :return: Instance of the adversarial report.
        """
        model_version_names = [
            model_version.name if isinstance(model_version, MLModelVersion) else model_version
            for model_version in model_versions
        ]
        dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
        subset_name = subset.name if isinstance(subset, Subset) else subset
        api_service = get_api_client()
        report = AdversarialReport(
            api_service=api_service,
            report_response=await ReportAPI(api_service).get_adversarial_report(
                request=ReportRequest(
                    model=model_name,
                    model_versions=model_version_names,
                    dataset=dataset_name,
                    subset=subset_name,
                    metrics=metrics,
                    success_metric_threshold=success_metric_threshold,
                )
            ),
        )
        report.model = model_name
        return report

    @staticmethod
    def _nested_dict_to_tuple_dict(
        nested_dict: Dict[str, Dict[str, Dict[str, ModelNormStats]]]
    ) -> Dict[Tuple[str, str, str], ModelNormStats]:
        return_dict: Dict[Tuple[str, str, str], ModelNormStats] = {}
        for index_1, dict_1 in nested_dict.items():
            for index_2, dict_2 in dict_1.items():
                for index_3, stats in dict_2.items():
                    return_dict[(index_1, index_2, index_3)] = stats
        return return_dict

    @classmethod
    def _get_model_comparison_stats(
        cls, stats_dict: Dict[str, Dict[str, Dict[str, Dict[str, ModelNormStats]]]]
    ) -> DataFrame:
        metrics_to_stat_mapper: Dict[Tuple[str, str, str, str], Dict[str, float]] = defaultdict(
            dict
        )
        for model_version, model_stats in stats_dict.items():
            for (
                distance_metric,
                success_metric,
                target_class,
            ), stats in cls._nested_dict_to_tuple_dict(model_stats).items():
                for stat_name, stat_value in stats:
                    metrics_to_stat_mapper[
                        (distance_metric, success_metric, target_class, stat_name)
                    ][model_version] = stat_value
        return DataFrame(metrics_to_stat_mapper)

    @classmethod
    def _get_attack_comparison_stats(
        cls,
        stats_dict: Dict[
            str, Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, ModelNormStats]]]]]
        ],
    ) -> Dict[str, DataFrame]:
        model_version_df_dict: Dict[str, DataFrame] = {}
        for model_version, attack_dict in stats_dict.items():
            stats_dict_in_pandas_form: Dict[
                Tuple[str, str, str, str], Dict[Tuple[str, str], float]
            ] = defaultdict(dict)
            for attack_class, attack_class_stats in attack_dict.items():
                for param_string, attack_instance_stats in attack_class_stats.items():
                    for (
                        distance_metric,
                        success_metric,
                        target_class,
                    ), stats in cls._nested_dict_to_tuple_dict(attack_instance_stats).items():
                        for stat_name, stat_value in stats.dict().items():
                            stats_dict_in_pandas_form[
                                (distance_metric, success_metric, target_class, stat_name)
                            ][(attack_class, param_string)] = stat_value
                        model_version_df_dict[model_version] = DataFrame(
                            data=stats_dict_in_pandas_form
                        )
        return model_version_df_dict

    @property
    def model_comparison_view(self) -> ModelComparisonView:
        """
        Get the model-comparison view of the report.

        :return: Model-comparison view containing a plot and summary statistics.
        """
        return ModelComparisonView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.model_comparison_asr)
            ),
            stats=self._get_model_comparison_stats(self._data.stats.model_comparison_stats),
        )

    @property
    def attack_comparison_view(self) -> AttackComparisonView:
        """
        Get the attack-comparison view of the report.

        :return: Attack-comparison view containing a plot and summary statistics.
        """
        return AttackComparisonView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.attack_comparison_asr)
            ),
            stats=self._get_attack_comparison_stats(
                stats_dict=self._data.stats.attack_comparison_stats
            ),
        )

    @property
    def attack_detail_view(self) -> AttackDetailView:
        """
        Get the attack-detail view of the report.

        :return: Attack-detail view containing a plot.
        """
        return AttackDetailView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.attack_detail_asr)
            )
        )

    async def fetch_random_inference_results(
        self, number_of_inference_results: int
    ) -> List[AdversarialExampleDetails]:
        """
        Fetch a number of random inference results for the adversarial examples
        of the report. If the report has fewer adversarial examples than
        specified, all inference results are returned.

        :param number_of_inference_results: Number of inference results to return.
        :return: List of inference details.
        """
        adversarial_example_ids = list(self.data["artifact_id"].unique())
        out = [
            await AdversarialExampleDetails.get_by_adversarial_example_id(adversarial_example_id)
            for adversarial_example_id in random.SystemRandom().sample(
                adversarial_example_ids,
                k=min(len(adversarial_example_ids), number_of_inference_results),
            )
        ]
        return out

    def _get_pipeline_info_for_id(self, adversarial_example_id: int) -> Dict:
        param_dict = json.loads(
            self.data[self.data["artifact_id"] == adversarial_example_id]["param_string"].iloc[0]
        )
        model_version = self.data[self.data["artifact_id"] == adversarial_example_id][
            "model_version"
        ].iloc[0]
        return {
            "Model": [f"Name: {self.model}<br>Version: {model_version}"],
            "Method Name": [
                self.data[self.data["artifact_id"] == adversarial_example_id]["method_name"].iloc[0]
            ],
            "Type": [
                self.data[self.data["artifact_id"] == adversarial_example_id][
                    "perturbation_type"
                ].iloc[0]
            ],
            "Parameters": [param_dict],
        }

    def _get_metrics_for_id(self, adversarial_example_id: int) -> Dict:
        metric_df = self.data[self.data["artifact_id"] == adversarial_example_id][
            ["distance_metric_name", "distance_metric_value"]
        ]
        metrics = {
            row["distance_metric_name"]: [f"{row['distance_metric_value']:.2f}"]
            for _, row in metric_df.iterrows()
        }
        return metrics

    async def get_detail_view(self, adversarial_example_id: int) -> widgets.VBox:
        """
        Return the detail for a given adversarial example.

        This method automatically selects the view corresponding to the model task.

        :param adversarial_example_id: ID specifying the adversarial example.
        :raises ValueError: If invalid output type is passed.
        :return: View as ipython widget.
        """
        if self._data.output_type == OutputType.CLASSIFICATION:
            return await self._get_classification_detail_view(
                adversarial_example_id=adversarial_example_id
            )
        if self._data.output_type == OutputType.SEGMENTATION:
            return await self._get_semantic_segmentation_detail_view(
                adversarial_example_id=adversarial_example_id
            )
        if self._data.output_type == OutputType.DETECTION:
            return await self._get_object_detection_detail_view(
                adversarial_example_id=adversarial_example_id
            )

        raise ValueError(
            "Unsupported output type. Should be one of 'CLASSIFICATION', 'SEGMENTATION'\
                or 'DETECTION'."
        )

    @staticmethod
    def _assemble_widgets_in_view(
        observation_widget: widgets.CoreWidget,
        widget_list: List[widgets.CoreWidget],
        widget_header: List[str],
    ) -> widgets.VBox:
        """
        Assemble the different widgets into a single view.

        :param observation_widget: Widget displaying the observations (possibly with inference).
        :param widget_list: List of widgets to display beneath the observations.
        :param widget_header: Titles for the widgets in widget_list.
        :return: The assembled view as widget.
        """
        header_widget = widgets.HTML(value="<h1>Detail View</h1>")

        acc_list = []
        for i, widget in enumerate(widget_list):
            acc = widgets.Accordion(children=[widget])
            acc.set_title(0, widget_header[i])

            acc.layout.width = "605px"
            acc_list.append(acc)
        return widgets.VBox([header_widget, observation_widget] + acc_list)

    async def _get_classification_detail_view(self, adversarial_example_id: int) -> widgets.VBox:
        """
        Produce the classification detail view for a given adversarial example.

        :raises ValueError: If inference output has wrong type.
        :param adversarial_example_id: ID specifying the adversarial example.
        :return: View as ipython widget.
        """
        artifact_details = await AdversarialExampleDetails.get_by_adversarial_example_id(
            adversarial_example_id
        )
        adversarial_example = (
            await artifact_details.adversarial_example_as_remote_file().fetch_remote_file()
        )
        observation_resource = await artifact_details.observation
        observation = await observation_resource.as_remote_file().fetch_remote_file()
        original_observation_widget = display_observation(
            observation,
            title="<center><b>Original Observation</b></center>",
            caption=[("File", observation_resource.name), ("ID", str(observation_resource.id))],
        )
        perturbed_observation_widget = display_observation(
            adversarial_example,
            title="<center><b>Perturbed Observation</b></center>",
            caption=[("ID", str(adversarial_example_id))],
        )

        if isinstance(observation, str):
            observation_box = widgets.VBox
        else:
            observation_box = widgets.HBox

        observation_box_widget = observation_box(
            [
                original_observation_widget,
                perturbed_observation_widget,
            ]
        )

        difference_widget = display_static_observation_difference(observation, adversarial_example)

        class_names = artifact_details.inference_class_names

        if not isinstance(
            artifact_details.observation_inference_result, ClassificationModelOutput
        ) or not isinstance(
            artifact_details.adversarial_example_inference_result, ClassificationModelOutput
        ):
            raise ValueError("Model task is wrongly configured.")

        observation_inference_result = artifact_details.observation_inference_result.data
        adversarial_example_inference_result = (
            artifact_details.adversarial_example_inference_result.data
        )

        top_inference_classes = (
            list(np.array(observation_inference_result).argsort())[-5:]
            + list(np.array(adversarial_example_inference_result).argsort())[-5:]
        )

        prediction_original = np.array(observation_inference_result).argmax()
        prediction_adversarial = np.array(adversarial_example_inference_result).argmax()

        inference_table: Dict[str, List[Union[str, float, int]]] = {
            str(class_names[i]): [
                f"{float(observation_inference_result[i]):.2f}",
                f"{float(adversarial_example_inference_result[i]):.2f}",
            ]
            for i in set(top_inference_classes)
        }
        inference_table_header = ["Original observation", "Perturbed observation"]
        prediction_highlight = {str(class_names[prediction_original]): {0: "#c0edc0"}}
        if prediction_original == prediction_adversarial:
            prediction_highlight[str(class_names[prediction_adversarial])][1] = "#c0edc0"
        else:
            prediction_highlight[str(class_names[prediction_adversarial])] = {1: "#c0edc0"}
        inference_table_widget = display_table(
            inference_table, header=inference_table_header, highlight_cells=prediction_highlight
        )
        metrics_table_widget = display_table(self._get_metrics_for_id(adversarial_example_id))
        pipeline_info_table_widget = display_table(
            self._get_pipeline_info_for_id(adversarial_example_id)
        )

        view_elements = [
            inference_table_widget,
            metrics_table_widget,
            pipeline_info_table_widget,
            difference_widget,
        ]
        view_element_headers = [
            "Model Inference",
            "Perturbation Size",
            "Perturbation Details",
            "Difference between Original and Perturbed Observation",
        ]

        return self._assemble_widgets_in_view(
            observation_box_widget, view_elements, view_element_headers
        )

    async def _get_semantic_segmentation_detail_view(
        self, adversarial_example_id: int
    ) -> widgets.VBox:
        """
        Produce the semantic segmentation detail view for a given adversarial
        example.

        :param adversarial_example_id: ID specifying the adversarial example.
        :return: View as ipython widget.
        """
        aversarial_example_details = await (
            AdversarialExampleDetails.get_by_adversarial_example_id(adversarial_example_id)
        )
        adversarial_example = await (
            aversarial_example_details.adversarial_example_as_remote_file().fetch_remote_file()
        )
        observation = (
            await (await aversarial_example_details.observation)
            .as_remote_file()
            .fetch_remote_file()
        )
        observation_resource = await aversarial_example_details.observation

        # Display the observation and the adversarial example side by side
        original_observation_widget = display_observation(
            observation,
            title="<center><b>Original Observation</b></center>",
            caption=[("File", observation_resource.name), ("ID", str(observation_resource.id))],
        )
        perturbed_observation_widget = display_observation(
            adversarial_example,
            title="<center><b>Perturbed Observation</b></center>",
            caption=[("ID", str(adversarial_example_id))],
        )

        observation_box_widget = widgets.HBox(
            [
                original_observation_widget,
                perturbed_observation_widget,
            ]
        )

        # Perform a fex computation to display in the detail view
        target_classes = aversarial_example_details.inference_class_names
        n_classes = len(target_classes)

        # Transform the inference data into numpy arrays
        inference_array = np.array(aversarial_example_details.observation_inference_result.data)
        perturbed_inference_array = np.array(
            aversarial_example_details.adversarial_example_inference_result.data
        )

        # Compute the images to show in the inference section of the detail view
        inference_per_class_confidence_images = get_inference_per_class_confidence(inference_array)
        perturbed_inference_per_class_confidence_images = get_inference_per_class_confidence(
            perturbed_inference_array
        )

        inference_argmax_image = get_inference_argmax_prediction(inference_array)
        perturbed_inference_argmax_image = get_inference_argmax_prediction(
            perturbed_inference_array
        )

        # Compute the coverage metrics
        inference_array_argmax = np.argmax(inference_array, axis=2)
        inference_array_perturbed_argmax = np.argmax(perturbed_inference_array, axis=2)

        coverage_original = (
            np.bincount(inference_array_argmax.flatten(), minlength=n_classes)
            / inference_array_argmax.size
        )
        coverage_perturbed = (
            np.bincount(inference_array_perturbed_argmax.flatten(), minlength=n_classes)
            / inference_array_perturbed_argmax.size
        )

        target_classes_properties = []
        target_classes_dropdown_options = []

        coverage_per_class: Dict[str, List[Union[str, float, int]]] = {}
        coverage_class_highlight: Dict[str, str] = {}

        # Iterate over the classes. Assign a color to them, create the dropdown
        # selector and prepare the coverage table.
        for i, target_class_name in enumerate(target_classes):

            color = display_class_color(i, n_classes, "turbo")
            target_classes_properties.append({"name": target_class_name, "color": color})

            target_classes_dropdown_options.append((target_class_name, i))

            coverage_per_class[target_class_name] = [
                f"{coverage_original[i]:.2%}",
                f"{coverage_perturbed[i]:.2%}",
            ]

            coverage_class_highlight[target_class_name] = color

        # All classes inference
        semantic_inference_widget = display_semantic_segmentation_inference_argmax_widget(
            observation,
            adversarial_example,
            inference_argmax_image,
            perturbed_inference_argmax_image,
            target_classes_properties,
        )

        # Specific class inference
        class_inference_per_class_widget = display_inference_per_class_widget(
            inference_per_class_confidence_images,
            perturbed_inference_per_class_confidence_images,
            target_classes_dropdown_options,
        )

        # Put the two inference widgets together
        inference_widget_tabs = widgets.Tab(
            children=[semantic_inference_widget, class_inference_per_class_widget]
        )
        for i, val in enumerate(["All classes", "Specific class"]):
            inference_widget_tabs.set_title(i, val)

        # Coverage widget
        coverage_table = display_table(
            data=coverage_per_class,
            header=["Original", "Perturbed"],
            table_width=500,
            highlight_row_header=coverage_class_highlight,
        )
        percentage_of_pixels_that_changed_class = (
            np.count_nonzero(inference_array_argmax - inference_array_perturbed_argmax)
            / inference_array_argmax.size
        )
        coverage_widget = widgets.VBox(
            [
                coverage_table,
                widgets.HTML(
                    value="<b>Percentage of pixels with changed prediction</b>: "
                    f"{percentage_of_pixels_that_changed_class:.2%}"
                ),
            ]
        )

        # Metrics widget
        metrics_table_widget = display_table(self._get_metrics_for_id(adversarial_example_id))
        pipeline_info_table_widget = display_table(
            self._get_pipeline_info_for_id(adversarial_example_id)
        )

        # Difference Widget
        difference_widget = display_static_observation_difference(observation, adversarial_example)

        view_elements = [
            inference_widget_tabs,
            coverage_widget,
            metrics_table_widget,
            pipeline_info_table_widget,
            difference_widget,
        ]
        view_element_headers = [
            "Model Inference",
            "Class Coverage",
            "Perturbation Size",
            "Perturbation Details",
            "Difference between Original and Perturbed Observation",
        ]

        return self._assemble_widgets_in_view(
            observation_box_widget, view_elements, view_element_headers
        )

    async def _get_object_detection_detail_view(self, adversarial_example_id: int) -> widgets.VBox:
        """
        Produce the object detection detail view for a given adversarial
        example.

        :raises ValueError: If inference output has wrong type.
        :param adversarial_example_id: ID specifying the adversarial example.
        :return: View as ipython widget.
        """
        artifact_details = await AdversarialExampleDetails.get_by_adversarial_example_id(
            adversarial_example_id
        )
        adversarial_example: PIL.Image.Image = (
            await artifact_details.adversarial_example_as_remote_file().fetch_remote_file()
        )
        observation_resource = await artifact_details.observation
        observation: PIL.Image.Image = (
            await observation_resource.as_remote_file().fetch_remote_file()
        )

        if not isinstance(
            artifact_details.observation_inference_result, ImageObjectDetectionModelOutput
        ) or not isinstance(
            artifact_details.adversarial_example_inference_result, ImageObjectDetectionModelOutput
        ):
            raise ValueError("Model task is wrongly configured.")

        observation_inference = artifact_details.observation_inference_result.data
        adversarial_example_inference = artifact_details.adversarial_example_inference_result.data

        observation_box_with_selector = display_selection_class_detection_widget(
            observation,
            adversarial_example,
            observation_inference,
            adversarial_example_inference,
            class_names=artifact_details.inference_class_names,
            observation_title="<center><b>Original Observation</b></center>",
            observation_caption=f"<center><b>File</b>: {observation_resource.name}, "
            f"<b>ID</b>: {observation_resource.id}</center>",
            perturbation_title="<center><b>Perturbed Observation</b></center>",
            perturbation_caption=f"<center><b>ID</b>: {adversarial_example_id}</center>",
        )

        difference_widget = display_static_observation_difference(observation, adversarial_example)

        box_count_widget = display_object_detection_box_count_widget(
            observation_inference,
            adversarial_example_inference,
            artifact_details.inference_class_names,
        )
        metrics_table_widget = display_table(self._get_metrics_for_id(adversarial_example_id))
        pipeline_info_table_widget = display_table(
            self._get_pipeline_info_for_id(adversarial_example_id)
        )

        view_elements = [
            box_count_widget,
            metrics_table_widget,
            pipeline_info_table_widget,
            difference_widget,
        ]
        view_element_headers = [
            "Bounding Boxes per Class",
            "Perturbation Size",
            "Perturbation Details",
            "Difference between Original and Perturbed Observation",
        ]

        return self._assemble_widgets_in_view(
            observation_box_with_selector, view_elements, view_element_headers
        )
