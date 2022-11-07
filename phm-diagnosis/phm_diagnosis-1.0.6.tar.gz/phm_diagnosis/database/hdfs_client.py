#!
from .base import DBInterface
from hdfs import Client

class HdfsClient(DBInterface):

    def __init__(self, hdfs_address):
        self.client = Client(hdfs_address)

    def read(self, path):
        content = self.client.read(path, encoding='utf-8')
        return content


