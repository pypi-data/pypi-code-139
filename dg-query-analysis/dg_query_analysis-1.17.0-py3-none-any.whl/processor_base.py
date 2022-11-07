import os
import json
from jieba.posseg import pair
import hashlib
from typing import Any



class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pair):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


class DataPackage(object):
    def __init__(self, **kwargs):
        self._data = {}
        self._data.update(kwargs)

    def get(self, key: str, default=None):
        _default = self._data.get(key, default)
        return self._data.get("req_params", {}).get(key, _default)

    def set(self, key: str, value: any):
        if key in self._data:
            self._data[key] = value
        if "req_params" in self._data and key in self._data["req_params"]:
            self._data["req_params"][key] = value

    def gets(self):
        return self._data

    def del_key(self, key):
        if key in self._data:
            del self._data[key]

    def merge(self, r):
        r_dict = r.gets()
        keys = set(r_dict.keys()) & set(self._data.keys())
        if len(keys):
            print('values for keys: %s updated ...' % " ".join(list(keys)))
        self._data.update(r.gets())

    update = merge

    def __str__(self):
        return json.dumps(self._data, indent=2, ensure_ascii=False, cls=UserEncoder)


class Output(DataPackage):
    def __init__(self, **kwargs):
        super(Output, self).__init__(**kwargs)


class Input(DataPackage):
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)


class ServerFlow(Output):
    def __init__(self, **kwargs):
        super(ServerFlow, self).__init__(**kwargs)


class MultiScene(list):
    pass


class ProcessorBase(object):
    def __init__(self, *args, **kwargs):

        # self.config = kwargs.get('config','config')
        # dgs_redis = DgsRedis(self.config)
        # redis_params = dgs_redis.get_redis_params()
        # g_rds_client = DgsDb(**redis_params)()
        # self._rds = g_rds_client
        pass

    def __str__(self):
        return ""

    def run(self, params: Input, *args, **kwargs):
        raise NotImplemented

    def _md5(self, key):
        if not isinstance(key, bytes):
            key = key.encode("utf8")
        m2 = hashlib.md5(key)
        return m2.hexdigest()

    def get_kwargs(self, kwargs):
        config = kwargs.get('config', None)
        rds = kwargs.get('g_rds_client', None)
        rds_mapping = kwargs.get('g_rds_mapping_dao', None)
        StockRecog = kwargs.get('StockRecog', None)
        return config, rds, rds_mapping, StockRecog



class ParaError(Exception):
    value: Any

# todo：参数：config, g_rds_client, g_rds_mapping_dao, StockRecog

