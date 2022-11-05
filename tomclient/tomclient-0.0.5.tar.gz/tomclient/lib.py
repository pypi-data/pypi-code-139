import asyncio
from jsonrpc_websocket import Server
from time import time 

class TOMClient():
    def __init__(self, host_url):
        self.server = Server(f"ws://{host_url}/api/v1/ws")

    def update_status(self, ip_addr: str, metric: str, value: str):
        current_time = int(time())
        async def send_status():
            await self.server.ws_connect()
            await self.server.worker_update_status(current_time, metric, value, ip_addr)
        asyncio.get_event_loop().run_until_complete(send_status())

    def join(self, worker_name: str, ip_addr: str, gpu_spec: str, gpu_memory: str):
        async def join_worker():
            await self.server.ws_connect()
            await self.server.worker_join(worker_name, ip_addr, gpu_spec, gpu_memory)
        asyncio.get_event_loop().run_until_complete(join_worker())