# coding: utf-8

from __future__ import absolute_import
import os
import math
import json
from six import iteritems
import time
from ..configuration import Configuration
from ..api_client import ApiClient


class UpLoadApi(object):
    """上传数据统一API.
    """

    def _init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def upload_tags(self, dataset_key, size, **kwargs):
        """获取DS数据集
        """
        pass

    def upload_dataset_with_http_info(self, dataset_key, size, **kwargs):
        pass
