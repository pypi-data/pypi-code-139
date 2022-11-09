import typing_extensions

from collibra_data_classification.apis.tags import TagValues
from collibra_data_classification.apis.tags.data_classification_api import DataClassificationApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.DATA_CLASSIFICATION: DataClassificationApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DATA_CLASSIFICATION: DataClassificationApi,
    }
)
