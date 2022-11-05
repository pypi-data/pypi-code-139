import dataclasses
from typing import List
import requests
from isaac_martin_sdk import sdk_config
from dataclasses_json import dataclass_json
import json
from isaac_martin_sdk.filter import Filter, Operator, operator_lookup


@dataclass_json
@dataclasses.dataclass
class ResourceBase:
    _default_headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get_endpoint():
        raise Exception('Implement Me')

    @staticmethod
    def requires_auth():
        return True

    @classmethod
    def _process_response(cls, response: requests.Response):
        if not response.ok:
            raise Exception(f'{response.status_code}: {response.content}')

        loaded = []
        content = json.loads(response.content)
        for obj in content['docs']:
            loaded.append(cls.from_dict(obj, infer_missing=True))
        return loaded


    @staticmethod
    def _build_auth_header():
        if sdk_config.AUTHENTICATION_TOKEN:
            raise Exception('You need an auth token. Make sure you have implemented the sdk (sdk.TheOneSDK) and provided an auth token')
        return {'Authorization': f'Bearer {sdk_config.AUTHENTICATION_TOKEN}'}

    @classmethod
    def make_request(cls, full_path:str):
        if cls.requires_auth():
            response = requests.get(full_path, headers=cls._default_headers | cls._build_auth_header())
        else:
            response = requests.get(full_path, headers=cls._default_headers)
        return response

    @classmethod
    def list(cls,
             limit: int = None,
             page: int = None,
             offset: int = None,
             sort: str = None,
             filters: List[Filter] = []
             ):
        '''
        :param limit: Limit the number of responses to your specified int.
        :param page: Select which page of responses you wish to return. Usually used in
        conjunction with `limit`
        :param offset: Move the start index of your response window up from it's normal starting point (`0`)
        :param sort: Sort by a specified field either descending or ascending. For example: `name:asc` or `name:dsc`
        :param filters: Filters modify the response according to the configuration of the filter.
        :return: A list of instances of the class implementing this method, retrieved from the remote api.
        '''
        full_path = f'{sdk_config.API_URL}{cls.get_endpoint()}'
        processed_response = cls._build_url_and_make_request(full_path=full_path,
                                                             limit=limit,
                                                             page=page,
                                                             offset=offset,
                                                             sort=sort,
                                                             filters=filters
                                                             )
        return processed_response

    @classmethod
    def _build_url_and_make_request(cls,
                                    full_path: str,
                                    limit: int = None,
                                    page: int = None,
                                    offset: int = None,
                                    sort: str = None,
                                    filters: List[Filter] = []):
        full_path = _apply_parameters(full_path=full_path,
                                      limit=limit,
                                      page=page,
                                      offset=offset,
                                      sort=sort,
                                      filters=filters)
        response = cls.make_request(full_path)
        return cls._process_response(response)

    @classmethod
    def index(cls,
              id:str,
              limit: int = None,
              page: int = None,
              offset: int = None,
              sort: str = None,
              filters: List[Filter] = []
              ):
        '''
        :param id: The identifier of the entity. Normally "_id" in the API response.
        :param limit: Limit the number of responses to your specified int.
        :param page: Select which page of responses you wish to return. Usually used in
        conjunction with `limit`
        :param offset: Move the start index of your response window up from it's normal starting point (`0`)
        :param sort: Sort by a specified field either descending or ascending. For example: `name:asc` or `name:dsc`
        :param filters: Filters modify the response according to the configuration of the filter.
        :return: A single instance of the class implementing this method, retrieved from the remote api.
        '''
        full_path = f'{sdk_config.API_URL}{cls.get_endpoint()}/{id}'
        processed_response = cls._build_url_and_make_request(full_path=full_path,
                                                             limit=limit,
                                                             page=page,
                                                             offset=offset,
                                                             sort=sort,
                                                             filters=filters
                                                             )
        return processed_response[0]


def apply_parameter(full_path: str,
                    name:str,
                    conjunction:bool,
                    parameter_value:object,
                    operator: str = '='):
    if parameter_value != None:
        if conjunction:
            full_path = f'{full_path}&{name}{operator}{parameter_value}'
        else:
            full_path = f'{full_path}{name}{operator}{parameter_value}'
        return full_path, True
    return full_path, False


def _apply_parameters(full_path:str,
                      limit: int = None,
                      page: int = None,
                      offset: int = None,
                      sort: str = None,
                      filters: List[Filter] = []):
    if limit or page or offset or sort or len(filters):
        full_path = f'{full_path}?'

    full_path, conjunction = apply_parameter(full_path=full_path, name='limit', conjunction=False, parameter_value=limit)
    full_path, conjunction = apply_parameter(full_path=full_path, name='offset', conjunction=conjunction, parameter_value=offset)
    full_path, conjunction = apply_parameter(full_path=full_path, name='page', conjunction=conjunction, parameter_value=page)
    full_path, conjunction = apply_parameter(full_path=full_path, name='sort', conjunction=conjunction, parameter_value=sort)

    for filter in filters:
        if filter.operator in [Operator.REGEX_MATCH, Operator.REGEX_NOT_MATCH]:
            filter.value = f'/{filter.value}/i'
        if filter.operator not in [Operator.EXISTS, Operator.NOT_EXISTS]:
            full_path, conjunction = apply_parameter(full_path=full_path,
                                                     name=filter.field,
                                                     conjunction=conjunction,
                                                     parameter_value=filter.value,
                                                     operator=operator_lookup[filter.operator])
        else:
            if conjunction:
                full_path = f'{full_path}&'
            if filter.operator == Operator.EXISTS:
                full_path = f'{full_path}{filter.field}'
            elif filter.operator == Operator.NOT_EXISTS:
                full_path = f'{full_path}!{filter.field}'
            conjunction = True
    return full_path

