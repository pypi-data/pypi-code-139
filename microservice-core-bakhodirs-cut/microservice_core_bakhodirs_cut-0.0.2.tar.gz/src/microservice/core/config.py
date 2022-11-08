import importlib


class Config(object):
    __instance = None
    env = None

    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)
        return Config.__instance

    @staticmethod
    def set_config(env):
        Config().env = env

    @staticmethod
    def get_config():
        return Config().env

    def __getattribute__(self, name):
        if name == "set_config" or name == "get_config" or name == "env":
            return super().__getattribute__(name)
        return getattr(self.env, name, None)


def init_conf(env):
    from .cdn import cdn_client

    config = importlib.import_module("config." + env)
    conf.set_config(config)
    cdn_client.create_client(conf)
    return conf


conf = Config()
