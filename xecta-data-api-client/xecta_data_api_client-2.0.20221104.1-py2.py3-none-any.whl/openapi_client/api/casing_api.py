"""
    Production API

    API exposing endpoints for managing well  and daily production.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from openapi_client.api_client import ApiClient, Endpoint
from openapi_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from openapi_client.model.casing import Casing
from openapi_client.model.casing_input import CasingInput


class CasingApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __delete_casing_by_source(
            self,
            source_well_id,
            source_wellbore_id,
            source_id,
            **kwargs
        ):
            """Delete casing records by source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_casing_by_source(source_well_id, source_wellbore_id, source_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):
                source_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                int
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            kwargs['source_id'] = \
                source_id
            return self.call_with_http_info(**kwargs)

        self.delete_casing_by_source = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}/casing/{sourceId}',
                'operation_id': 'delete_casing_by_source',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                    'source_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
                    'source_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                    'source_wellbore_id':
                        (str,),
                    'source_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                    'source_id': 'sourceId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
                    'source_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__delete_casing_by_source
        )

        def __delete_casing_by_source_well(
            self,
            source_well_id,
            **kwargs
        ):
            """Delete casing records by well source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_casing_by_source_well(source_well_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                int
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            return self.call_with_http_info(**kwargs)

        self.delete_casing_by_source_well = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/casing',
                'operation_id': 'delete_casing_by_source_well',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                ],
                'required': [
                    'source_well_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                },
                'location_map': {
                    'source_well_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__delete_casing_by_source_well
        )

        def __delete_casing_by_source_wellbore(
            self,
            source_well_id,
            source_wellbore_id,
            **kwargs
        ):
            """Delete casing records by well source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_casing_by_source_wellbore(source_well_id, source_wellbore_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                int
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            return self.call_with_http_info(**kwargs)

        self.delete_casing_by_source_wellbore = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}/casing',
                'operation_id': 'delete_casing_by_source_wellbore',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                    'source_wellbore_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__delete_casing_by_source_wellbore
        )

        def __get_casing_by_source(
            self,
            source_well_id,
            source_wellbore_id,
            source_id,
            **kwargs
        ):
            """Get a casing record by source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_casing_by_source(source_well_id, source_wellbore_id, source_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):
                source_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                Casing
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            kwargs['source_id'] = \
                source_id
            return self.call_with_http_info(**kwargs)

        self.get_casing_by_source = Endpoint(
            settings={
                'response_type': (Casing,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}/casing/{sourceId}',
                'operation_id': 'get_casing_by_source',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                    'source_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
                    'source_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                    'source_wellbore_id':
                        (str,),
                    'source_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                    'source_id': 'sourceId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
                    'source_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_casing_by_source
        )

        def __get_casing_by_source_well(
            self,
            source_well_id,
            **kwargs
        ):
            """Fetch casing records by source well id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_casing_by_source_well(source_well_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [Casing]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            return self.call_with_http_info(**kwargs)

        self.get_casing_by_source_well = Endpoint(
            settings={
                'response_type': ([Casing],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/casing',
                'operation_id': 'get_casing_by_source_well',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                ],
                'required': [
                    'source_well_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                },
                'location_map': {
                    'source_well_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_casing_by_source_well
        )

        def __get_casing_by_source_wellbore(
            self,
            source_well_id,
            source_wellbore_id,
            **kwargs
        ):
            """Fetch casing records by source wellbore id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_casing_by_source_wellbore(source_well_id, source_wellbore_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [Casing]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            return self.call_with_http_info(**kwargs)

        self.get_casing_by_source_wellbore = Endpoint(
            settings={
                'response_type': ([Casing],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}/casing',
                'operation_id': 'get_casing_by_source_wellbore',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                    'source_wellbore_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_casing_by_source_wellbore
        )

        def __upsert_casing(
            self,
            casing_input,
            **kwargs
        ):
            """Bulk Add / Update Casing Data  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upsert_casing(casing_input, async_req=True)
            >>> result = thread.get()

            Args:
                casing_input ([CasingInput]):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [Casing]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['casing_input'] = \
                casing_input
            return self.call_with_http_info(**kwargs)

        self.upsert_casing = Endpoint(
            settings={
                'response_type': ([Casing],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/casing',
                'operation_id': 'upsert_casing',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'casing_input',
                ],
                'required': [
                    'casing_input',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'casing_input':
                        ([CasingInput],),
                },
                'attribute_map': {
                },
                'location_map': {
                    'casing_input': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__upsert_casing
        )
