from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.response_listmodels_interval_price import ResponseListmodelsIntervalPrice
from ...types import UNSET, Response


def _get_kwargs(
    symbol: str,
    date: str,
    *,
    client: Client,
    access_key: str,
) -> Dict[str, Any]:
    url = "{}/tickers/{symbol}/intraday/{date}".format(
        client.base_url, symbol=symbol, date=date
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["access_key"] = access_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    if response.status_code == 200:
        response_200 = ResponseListmodelsIntervalPrice.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    symbol: str,
    date: str,
    *,
    client: Client,
    access_key: str,
) -> Response[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    """Symbol Intraday Date

    Args:
        symbol (str):
        date (str): Date in the formats %Y-%m-%d, %Y-%m-%d %H:%M:%S or ISO-8601
            %Y-%m-%dT%H:%M:%S+%Z
        access_key (str):

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        date=date,
        client=client,
        access_key=access_key,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    symbol: str,
    date: str,
    *,
    client: Client,
    access_key: str,
) -> Optional[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    """Symbol Intraday Date

    Args:
        symbol (str):
        date (str): Date in the formats %Y-%m-%d, %Y-%m-%d %H:%M:%S or ISO-8601
            %Y-%m-%dT%H:%M:%S+%Z
        access_key (str):

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]]
    """

    return sync_detailed(
        symbol=symbol,
        date=date,
        client=client,
        access_key=access_key,
    ).parsed


async def asyncio_detailed(
    symbol: str,
    date: str,
    *,
    client: Client,
    access_key: str,
) -> Response[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    """Symbol Intraday Date

    Args:
        symbol (str):
        date (str): Date in the formats %Y-%m-%d, %Y-%m-%d %H:%M:%S or ISO-8601
            %Y-%m-%dT%H:%M:%S+%Z
        access_key (str):

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]]
    """

    kwargs = _get_kwargs(
        symbol=symbol,
        date=date,
        client=client,
        access_key=access_key,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    symbol: str,
    date: str,
    *,
    client: Client,
    access_key: str,
) -> Optional[
    Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]
]:
    """Symbol Intraday Date

    Args:
        symbol (str):
        date (str): Date in the formats %Y-%m-%d, %Y-%m-%d %H:%M:%S or ISO-8601
            %Y-%m-%dT%H:%M:%S+%Z
        access_key (str):

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, ResponseListmodelsIntervalPrice]]
    """

    return (
        await asyncio_detailed(
            symbol=symbol,
            date=date,
            client=client,
            access_key=access_key,
        )
    ).parsed
