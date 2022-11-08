import base64

from .annotation import Annotation
from .constants import BOX_ANNOTATION, POLYGON_ANNOTATION, LINE_ANNOTATION
from .datalakeinterface import DatalakeInterface
from .logger import get_debug_logger
from .model import Model

datalake_logger = get_debug_logger('DatalakeClient')


class DatalakeClient:
    """
    Python SDK of Datalake
    """

    def __init__(self, encoded_key_secret: str, layerx_url: str) -> None:
        _datalake_url = f'{layerx_url}/datalake'
        self.datalake_interface = DatalakeInterface(encoded_key_secret, _datalake_url)

    def upload_annotation_from_cocojson(self, file_path: str):
        """
        available soon
        """
        datalake_logger.debug(f'file_name={file_path}')
        _annotation = Annotation(client=self)
        _annotation.upload_coco(file_path)

    def upload_modelrun_from_json(
            self,
            storage_base_path: str,
            model_id: str,
            file_path: str,
            annotation_geometry: str
    ):
        datalake_logger.debug(f'upload_modelrun_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _model = Model(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, BOX_ANNOTATION)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, POLYGON_ANNOTATION)
        elif annotation_geometry == LINE_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, LINE_ANNOTATION)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    # def upload_modelrun_bbox_from_json(self, storage_base_path: str, model_id: str, file_path: str):
    #     """
    #     Upload model run data of boxes from a json file
    #     """
    #     datalake_logger.debug(f'file_name={file_path}')
    #     _model = Model(client=self)
    #     _model.upload_modelrun_json(storage_base_path, model_id, file_path, BOX_ANNOTATION)
    #
    # def upload_modelrun_polygon_from_json(self, storage_base_path: str, model_id: str, file_path: str):
    #     """
    #     Upload model run data of polygons from a json file
    #     """
    #     datalake_logger.debug(f'file_name={file_path}')
    #     _model = Model(client=self)
    #     _model.upload_modelrun_json(storage_base_path, model_id, file_path, POLYGON_ANNOTATION)
    #
    # def upload_modelrun_line_from_json(self, storage_base_path: str, model_id: str, file_path: str):
    #     """
    #     Upload model run data of lines from a json file
    #     """
    #     datalake_logger.debug(f'file_name={file_path}')
    #     _model = Model(client=self)
    #     _model.upload_modelrun_json(storage_base_path, model_id, file_path, LINE_ANNOTATION)
