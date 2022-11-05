from __future__ import annotations
from isaac_martin_sdk.resources.base_resource import ResourceBase
from dataclasses import dataclass
from isaac_martin_sdk import sdk_config
from typing import List
from isaac_martin_sdk.filter import Filter
from isaac_martin_sdk.resources.chapter import Chapter


@dataclass
class Book(ResourceBase):
    _id: str
    name: str

    @staticmethod
    def get_endpoint():
        '''
        Override the superclass method to return this class's specific endpoint.
        :return:
        '''
        return '/book'

    @staticmethod
    def requires_auth():
        return False

    @classmethod
    def chapters(cls,
                 book_id: str,
                 limit: int = None,
                 page: int = None,
                 offset: int = None,
                 sort: str = None,
                 filters: List[Filter] = []
                 ) -> List[Chapter]:
        '''
        :param book_id: The identifier of the entity. Normally "_id" in the API response.
        :param limit: Limit the number of responses to your specified int.
        :param page: Select which page of responses you wish to return. Usually used in
        conjunction with `limit`
        :param offset: Move the start index of your response window up from it's normal starting point (`0`)
        :param sort: Sort by a specified field either descending or ascending. For example: `name:asc` or `name:dsc`
        :param filters: Filters modify the response according to the configuration of the filter.
        :return: A list chapters, retrieved from the remote api.
        '''
        full_path = f'{sdk_config.API_URL}{cls.get_endpoint()}/{book_id}/chapter'
        processed_response = Chapter._build_url_and_make_request(full_path=full_path,
                                                                 limit=limit,
                                                                 page=page,
                                                                 offset=offset,
                                                                 sort=sort,
                                                                 filters=filters
                                                                 )
        return processed_response

