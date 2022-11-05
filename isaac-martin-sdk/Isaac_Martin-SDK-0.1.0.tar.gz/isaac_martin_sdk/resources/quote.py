from isaac_martin_sdk.resources.base_resource import ResourceBase
from dataclasses import dataclass


@dataclass
class Quote(ResourceBase):
    _id: str
    dialog: str
    movie: str
    character: str

    @staticmethod
    def get_endpoint():
        '''
        Override the superclass method to return this class's specific endpoint.
        :return:
        '''
        return '/quote'
