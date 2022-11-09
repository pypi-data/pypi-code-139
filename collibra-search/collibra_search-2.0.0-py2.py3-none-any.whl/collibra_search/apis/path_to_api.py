import typing_extensions

from collibra_search.paths import PathValues
from collibra_search.apis.paths.search_views import SearchViews
from collibra_search.apis.paths.search_views_view_id import SearchViewsViewId
from collibra_search.apis.paths.search import Search

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.SEARCH_VIEWS: SearchViews,
        PathValues.SEARCH_VIEWS_VIEW_ID: SearchViewsViewId,
        PathValues.SEARCH: Search,
    }
)

path_to_api = PathToApi(
    {
        PathValues.SEARCH_VIEWS: SearchViews,
        PathValues.SEARCH_VIEWS_VIEW_ID: SearchViewsViewId,
        PathValues.SEARCH: Search,
    }
)
