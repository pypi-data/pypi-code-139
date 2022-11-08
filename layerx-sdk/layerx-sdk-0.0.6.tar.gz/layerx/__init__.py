import base64
from layerx import datalake
from layerx import dataset


class LayerxClient:
    """
    Python SDK of LayerX
    """

    def __init__(self, api_key: str, secret: str, layerx_url: str) -> None:
        _string_key_secret = f'{api_key}:{secret}'
        _key_secret_bytes = _string_key_secret.encode("ascii")
        _encoded_key_secret_bytes = base64.b64encode(_key_secret_bytes)
        self.encoded_key_secret = _encoded_key_secret_bytes.decode("ascii")
        self.layerx_url = layerx_url


    def upload_modelrun_from_json(self, storage_base_path: str, model_id: str, file_path: str, annotation_geometry: str):
        """
        Upload model run data from a json file
        """
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)

        _datalake_client.upload_modelrun_from_json(storage_base_path,  model_id, file_path, annotation_geometry)


    """
    Download dataset """
    def download_dataset(self, version_id: str, export_type: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_dataset(version_id, export_type)


    """
    Download collection annotations
    From datalake
    @param collection_id - id of dataset version """
    def download_collection(self, collection_id: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_collection(collection_id)
