from isaac_martin_sdk.resources.base_resource import ResourceBase
from dataclasses import dataclass
from isaac_martin_sdk import sdk_config
from isaac_martin_sdk.filter import Filter
from typing import List
from isaac_martin_sdk.resources.quote import Quote


@dataclass
class Character(ResourceBase):
    _id: str
    height: str
    race: str
    gender: str
    birth: str
    spouse: str
    death: str
    realm: str
    hair: str
    name: str
    wikiUrl: str

    @staticmethod
    def get_endpoint():
        '''
        Override the superclass method to return this class's specific endpoint.
        :return:
        '''
        return '/character'

    @classmethod
    def quotes(cls,
               character_id: str,
               limit: int = None,
               page: int = None,
               offset: int = None,
               sort: str = None,
               filters: List[Filter] = []
               ) -> List[Quote]:
        '''
        :param character_id: The identifier of the entity. Normally "_id" in the API response.
        :param limit: Limit the number of responses to your specified int.
        :param page: Select which page of responses you wish to return. Usually used in
        conjunction with `limit`
        :param offset: Move the start index of your response window up from it's normal starting point (`0`)
        :param sort: Sort by a specified field either descending or ascending. For example: `name:asc` or `name:dsc`
        :param filters: Filters modify the response according to the configuration of the filter.
        :return: A list of quotes, retrieved from the remote api.
        '''
        full_path = f'{sdk_config.API_URL}{cls.get_endpoint()}/{character_id}/quote'
        processed_response = Quote._build_url_and_make_request(full_path=full_path,
                                                               limit=limit,
                                                               page=page,
                                                               offset=offset,
                                                               sort=sort,
                                                               filters=filters
                                                               )
        return processed_response

