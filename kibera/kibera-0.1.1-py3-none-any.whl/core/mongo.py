import logging
import os
import random
import re
import threading
from urllib.parse import urlparse

import portforward
import pymongo

logger = logging.getLogger(__name__)

mongo_db_name = "kibera"


class DBError(Exception):
    pass


class DBProxy:
    _db = None
    _mongo_url = None
    _forward_port = 27018 + random.randint(1, 1000)
    _forward_ctx = None

    def _connect(self):
        if not self._mongo_url:
            raise ValueError("Mongo URL has not been set")

        logger.debug("Connecting to mongodb at %s", self._mongo_url)
        client = pymongo.MongoClient(self._mongo_url)
        self._db = client[mongo_db_name]

    def set_url(self, u):
        self._mongo_url = u

    def __getattr__(self, key):
        if self._db is None:
            self._connect()
        return getattr(self._db, key)


db = DBProxy()
