import asyncio
from pprint import pprint
import json
from typing import Any, List, Optional, Dict
import async_timeout
import aiohttp
from dockerode_api_proxy_client.middleware.json_web_token_middleware import (
    jwt_authenticate,
)
from dockerode_api_proxy_client.settings.env import get_environment_enum
from dockerode_api_proxy_client.dto.image import ImageInfo
from dockerode_api_proxy_client.dto.container import ContainerInfo, ContainerInspectInfo
from dockerode_api_proxy_client.utils.formatting import camel_case_keys, define_dict


class ApiProxyClient:
    def __init__(
        self,
        host: str = "https://proxy.caesari.se",
        request_timeout: int = 10,
        default_headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    ) -> None:
        self._host = host
        self._request_timeout = request_timeout
        self._default_headers = default_headers

    def _construct_url(self, path: str) -> str:
        return f"{self._host}/v1/{path}"

    async def _parse_response(self, response: aiohttp.ClientResponse):
        if response.status != 200:
            return response.raise_for_status()
        text = await response.text()
        try:
            data = json.loads(text)
            return data
        except json.decoder.JSONDecodeError:
            return text

    @jwt_authenticate(get_environment_enum().JWT_SECRET)
    async def _get(self, path: str, params: Dict[str, str] = {}, *args, **kwargs):
        request_url = self._construct_url(path)
        async with aiohttp.ClientSession(headers=self._default_headers) as session:
            async with async_timeout.timeout(self._request_timeout):
                async with session.get(
                    request_url, params=params, *args, **kwargs
                ) as response:
                    return await self._parse_response(response)

    @jwt_authenticate(get_environment_enum().JWT_SECRET)
    async def _post(self, path: str, data: Dict[str, Any] = {}, *args, **kwargs):
        request_url = self._construct_url(path)
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self._request_timeout):
                async with session.post(
                    request_url, json=data, *args, **kwargs
                ) as response:
                    return await self._parse_response(response)

    @jwt_authenticate(get_environment_enum().JWT_SECRET)
    async def _delete(self, path: str, params: Dict[str, str] = {}, *args, **kwargs):
        request_url = self._construct_url(path)
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self._request_timeout):
                async with session.delete(
                    request_url, params=params, *args, **kwargs
                ) as response:
                    return await self._parse_response(response)

    async def get_all_images(self, *args, **kwargs) -> List[ImageInfo]:
        response = await self._get(path="image", *args, **kwargs)
        result: List[ImageInfo] = list(map(lambda entry: ImageInfo(**entry), response))
        return result

    async def get_all_containers(self, *args, **kwargs) -> List[ContainerInfo]:
        response = await self._get(path="container", *args, **kwargs)
        result: List[ContainerInfo] = list(
            map(lambda entry: ContainerInfo(**entry), response)
        )
        return result

    async def get_container_by_id(self, id: str, *args, **kwargs) -> str:
        response = await self._get(path=f"container/{id}", *args, **kwargs)
        return response

    async def inspect_container_by_id(
        self, id: str, *args, **kwargs
    ) -> ContainerInspectInfo:
        response = await self._get(path=f"container/{id}/inspect", *args, **kwargs)
        result: ContainerInspectInfo = ContainerInspectInfo(**response)
        return result

    async def create(
        self,
        image: str,
        env: List[str],
        name: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        exposed_ports: Optional[Dict[str, Dict[str, None]]] = None,
        keep_alive: Optional[bool] = None,
        *args,
        **kwargs,
    ):
        defined_params = {
            "image": image,
            "env": env,
            "name": name,
            "labels": labels,
            "exposed_ports": exposed_ports,
            "keep_alive": keep_alive,
        }
        create_params = camel_case_keys(define_dict(defined_params))
        response = await self._post(
            path="container/create", data=create_params, *args, **kwargs
        )
        return response

    async def start(self, id: str, *args, **kwargs):
        response = await self._post(path=f"container/{id}/start", *args, **kwargs)
        return response

    async def pause(self, id: str, *args, **kwargs):
        response = await self._post(path=f"container/{id}/pause", *args, **kwargs)
        return response

    async def restart(self, id: str, *args, **kwargs):
        response = await self._post(path=f"container/{id}/restart", *args, **kwargs)
        return response

    async def stop(self, id: str, *args, **kwargs):
        response = await self._post(path=f"container/{id}/stop", *args, **kwargs)
        return response

    async def remove(self, id: str, *args, **kwargs):
        response = await self._delete(path=f"container/{id}", *args, **kwargs)
        return response


async def main():
    client = ApiProxyClient(host="http://localhost:6000")
    response = await client.get_all_containers()
    pprint(response)


if __name__ == "__main__":
    asyncio.run(main())
