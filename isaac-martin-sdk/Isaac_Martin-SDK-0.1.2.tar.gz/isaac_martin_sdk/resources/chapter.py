from __future__ import annotations
from isaac_martin_sdk.resources.base_resource import ResourceBase
from dataclasses import dataclass


@dataclass
class Chapter(ResourceBase):
    _id: str
    chapterName: str

    @staticmethod
    def get_endpoint():
        '''
        Override the superclass method to return this class's specific endpoint.
        :return:
        '''
        return '/chapter'
