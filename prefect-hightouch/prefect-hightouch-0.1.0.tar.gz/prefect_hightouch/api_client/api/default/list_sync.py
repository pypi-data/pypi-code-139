"""
This is a module containing functions, auto-generated from the 
REST schema, but note these are **not** Prefect tasks.

Example usage shown below; be sure to replace `endpoint_fn` with the desired endpoint function.

```python
from prefect_hightouch.credentials import HightouchCredentials
from prefect_hightouch.api_client.api.default import endpoint_fn

credentials = HightouchCredentials(token="my-service-token")
client = credentials.get_client()
result = endpoint_fn.sync(client=client)
```

The functions are described below:

- `asyncio`: Non-blocking request that returns parsed data (if successful) or None. Any calls must be awaited.
- `asyncio_detailed`: Non-blocking request that always returns a Request, optionally with parsed set if the request was successful. Any calls must be awaited.
- `sync`: Blocking request that returns parsed data (if successful) or None.
- `sync_detailed`: Blocking request that always returns a Request, optionally with parsed set if the request was successful.
"""

import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.list_sync_order_by import ListSyncOrderBy
from ...models.list_sync_response_200 import ListSyncResponse200
from ...models.validate_error_json import ValidateErrorJSON
from ...types import UNSET, Response, Unset


def _get_kwargs(
    client: AuthenticatedClient,
    slug: Union[Unset, None, str] = UNSET,
    model_id: Union[Unset, None, float] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    order_by: Union[Unset, None, ListSyncOrderBy] = ListSyncOrderBy.ID,
) -> Dict[str, Any]:
    url = "{}/syncs".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["slug"] = slug

    params["modelId"] = model_id

    json_after: Union[Unset, None, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat() if after else None

    params["after"] = json_after

    json_before: Union[Unset, None, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat() if before else None

    params["before"] = json_before

    params["limit"] = limit

    json_order_by: Union[Unset, None, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value if order_by else None

    params["orderBy"] = json_order_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    kwargs = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }

    if "json" in kwargs:
        kwargs["json"] = {k: v for k, v in kwargs["json"].items() if v != UNSET}
    return kwargs


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListSyncResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidateErrorJSON.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    response.raise_for_status()

    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    client: AuthenticatedClient,
    slug: Union[Unset, None, str] = UNSET,
    model_id: Union[Unset, None, float] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    order_by: Union[Unset, None, ListSyncOrderBy] = ListSyncOrderBy.ID,
) -> Response[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    """List Syncs

     List all the syncs in the current workspace

    Args:
        client: An authenticated client.
        slug (Union[Unset, None, str]):
        model_id (Union[Unset, None, float]):
        after (Union[Unset, None, datetime.datetime]):
        before (Union[Unset, None, datetime.datetime]):
        limit (Union[Unset, None, float]):
        order_by (Union[Unset, None, ListSyncOrderBy]):  Default: ListSyncOrderBy.ID.

    Returns:
        The response.
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        model_id=model_id,
        after=after,
        before=before,
        limit=limit,
        order_by=order_by,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    client: AuthenticatedClient,
    slug: Union[Unset, None, str] = UNSET,
    model_id: Union[Unset, None, float] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    order_by: Union[Unset, None, ListSyncOrderBy] = ListSyncOrderBy.ID,
) -> Optional[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    """List Syncs

     List all the syncs in the current workspace

    Args:
        client: An authenticated client.
        slug (Union[Unset, None, str]):
        model_id (Union[Unset, None, float]):
        after (Union[Unset, None, datetime.datetime]):
        before (Union[Unset, None, datetime.datetime]):
        limit (Union[Unset, None, float]):
        order_by (Union[Unset, None, ListSyncOrderBy]):  Default: ListSyncOrderBy.ID.

    Returns:
        The parsed response.
    """

    return sync_detailed(
        client=client,
        slug=slug,
        model_id=model_id,
        after=after,
        before=before,
        limit=limit,
        order_by=order_by,
    ).parsed


async def asyncio_detailed(
    client: AuthenticatedClient,
    slug: Union[Unset, None, str] = UNSET,
    model_id: Union[Unset, None, float] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    order_by: Union[Unset, None, ListSyncOrderBy] = ListSyncOrderBy.ID,
) -> Response[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    """List Syncs

     List all the syncs in the current workspace

    Args:
        client: An authenticated client.
        slug (Union[Unset, None, str]):
        model_id (Union[Unset, None, float]):
        after (Union[Unset, None, datetime.datetime]):
        before (Union[Unset, None, datetime.datetime]):
        limit (Union[Unset, None, float]):
        order_by (Union[Unset, None, ListSyncOrderBy]):  Default: ListSyncOrderBy.ID.

    Returns:
        The response.
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        model_id=model_id,
        after=after,
        before=before,
        limit=limit,
        order_by=order_by,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    client: AuthenticatedClient,
    slug: Union[Unset, None, str] = UNSET,
    model_id: Union[Unset, None, float] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    order_by: Union[Unset, None, ListSyncOrderBy] = ListSyncOrderBy.ID,
) -> Optional[Union[Any, ListSyncResponse200, ValidateErrorJSON]]:
    """List Syncs

     List all the syncs in the current workspace

    Args:
        client: An authenticated client.
        slug (Union[Unset, None, str]):
        model_id (Union[Unset, None, float]):
        after (Union[Unset, None, datetime.datetime]):
        before (Union[Unset, None, datetime.datetime]):
        limit (Union[Unset, None, float]):
        order_by (Union[Unset, None, ListSyncOrderBy]):  Default: ListSyncOrderBy.ID.

    Returns:
        The parsed response.
    """

    return (
        await asyncio_detailed(
            client=client,
            slug=slug,
            model_id=model_id,
            after=after,
            before=before,
            limit=limit,
            order_by=order_by,
        )
    ).parsed
