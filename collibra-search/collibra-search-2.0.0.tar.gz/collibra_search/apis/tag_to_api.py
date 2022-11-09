import typing_extensions

from collibra_search.apis.tags import TagValues
from collibra_search.apis.tags.search_api import SearchApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.SEARCH: SearchApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.SEARCH: SearchApi,
    }
)
