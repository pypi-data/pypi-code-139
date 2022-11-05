"""
Contains a `ProcessRequest` class to process and get a response
from a given route and requested method. Use to process client requests.
"""

import http_pyparser
from typing import List, Union

from .route import Route
from .status import status
from .server import Client


class RequestData:
    def __init__(
        self,
        parsed_http: http_pyparser.parser.HTTPData,
        remote_addr: tuple,
        parameters: dict
    ):
        self.real_path = parsed_http.real_path

        self.path = parsed_http.path
        self.method = parsed_http.method
        self.version = parsed_http.version
        
        self.host = parsed_http.host
        self.user_agent = parsed_http.user_agent
        self.accept = parsed_http.accept

        self.body = parsed_http.body
        self.headers = parsed_http.headers
        self.cookies = parsed_http.cookies
        self.query = parsed_http.query

        self.remote_addr = remote_addr
        self.parameters = parameters

    def __repr__(self) -> str:
        return (f'RequestData(real_path="{self.real_path}", path="{self.path}", method="{self.method}", '
                f'version="{self.version}", host="{self.host}", user_agent="{self.user_agent}", '
                f'accept="{self.accept}", body={self.body}, headers={self.headers}, cookies={self.cookies}, '
                f'query={self.query}, remote_addr={self.remote_addr}, parameters={self.parameters})')


class ProcessRequest:
    def __init__(self, routes: List[Route]) -> None:
        self._routes = routes

    def process(self, client: Client) -> Union[http_pyparser.Response, bool]:
        """Process and get or create a response to
        specified path and requested method.

        The HTTP message is obtained by `Client`
        class; the `http_pyparser` library parse this
        and return a class with HTTP data.

        :param client: A `Client` instance
        :type client: Client
        :return: Return request response
        :rtype: Union[http_pyparser.Response, bool]
        """

        # get client request
        message = client.get_message()

        if not message:
            client.destroy()
            response = False
        else:
            http_parser = http_pyparser.parser.HTTPParser()
            parsed_http = http_parser.parser(message)

            match_route: Route = None

            # checking routes
            for route in self._routes:
                parameters = route.get_parameters(parsed_http.path)

                if route.match_route(parsed_http.path) or parameters is not False:
                    match_route = route
                    break

            # make route response
            if match_route:
                remote_addr = client.get_address()
                request = RequestData(parsed_http, remote_addr, parameters)

                if route.accept_method(request.method):
                    response = route.get_route_response(request)
                else:
                    response = http_pyparser.response.Response(
                        body='Method Not Allowed',
                        status=status.method_not_allowed_405
                    )
            else:
                response = http_pyparser.response.Response(
                    body='Not Found',
                    status=status.not_found_404
                )

        return response
