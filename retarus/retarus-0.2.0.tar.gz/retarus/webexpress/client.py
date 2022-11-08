from typing import List

from ..common.region import RegionUri, Region
from ._async import AsyncWebExpressClient
from .sync import SyncWebExpressClient


class WebExpressClient(object):
    __express_uris: List[RegionUri] = [
        RegionUri(
            region=Region.Europe,
            ha_uri="https://webexpress.retarus.com/PicoPortal/autoLogin/listImport",
            urls=[]
        )
    ]

    def __init__(self, is_async: bool = False):
        self.is_async = is_async
        if is_async:
            self.client = AsyncWebExpressClient(self.__express_uris)
        else:
            self.client = SyncWebExpressClient(self.__express_uris)