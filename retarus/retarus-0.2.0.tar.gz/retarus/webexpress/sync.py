import asyncio

from ._async import AsyncWebExpressClient
from .models import Client


class SyncWebExpressClient(Client):
    def __init__(self, uris):
        self.uris = uris
        self.client = AsyncWebExpressClient(self.uris)
        self.loop = asyncio.new_event_loop()
    
    def upload_distributor_list(self, payload):
        """
        Takes your [ListImport] and sends it to the server, where is determine if the syntax of your submitted file is correct.
        """
        res = self.loop.run_until_complete(self.client.upload_distributor_list(payload))
        return res