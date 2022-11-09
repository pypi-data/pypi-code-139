import typing_extensions

from collibra_importer.apis.tags import TagValues
from collibra_importer.apis.tags.model_import_api import ModelImportApi
from collibra_importer.apis.tags.import_results_api import ImportResultsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.IMPORT: ModelImportApi,
        TagValues.IMPORT_RESULTS: ImportResultsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.IMPORT: ModelImportApi,
        TagValues.IMPORT_RESULTS: ImportResultsApi,
    }
)
