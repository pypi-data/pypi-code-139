from engine import utils
from engine import constants
from engine.protocols import Client

CONTAINER = constants.CONTAINER
SYNC_GROUPS = constants.SYNC_GROUPS
SUPER_SYNC_GROUPS = constants.SUPER_SYNC_GROUPS
SUPER_CONTAINER = constants.SUPER_CONTAINER


class StationConfiguration(object):
    def __init__(self, name=None, cont=None):
        self._name = name
        self.cont = cont if cont else {}

    def add_container(self, name):
        self.cont[self._name]['containers'].append(name) if self.cont else None
        CONTAINER[name] = {}
        return StationConfiguration(name, self.cont)

    def add_super_container(self, name, timeout=0, shared_conn=True):
        SUPER_CONTAINER[self._name].update({'shared_conn': shared_conn, 'sync_group': name})
        self.cont.update({name: {'timeout': timeout, 'containers': []}})
        return StationConfiguration(name, self.cont)

    def add_connection(self, name, **kwargs):
        if self._name:
            CONTAINER[self._name].update({name: kwargs, **SUPER_CONTAINER})
        else:
            self._name = name
            SUPER_CONTAINER.update({self._name: kwargs})
            CONTAINER.update({self._name: kwargs})

    def add_sync_group(self, name, containers, timeout=60):
        containers = [cont.__dict__['_name'] for cont in containers]
        [[CONTAINER[c][i].update({'sync_group': name}) for i in CONTAINER[c] if i != self._name] for c in containers]
        SUPER_SYNC_GROUPS.update(self.cont) if self.cont else None
        [SYNC_GROUPS.update({container: {'name': name,
                                         'timeout': timeout,
                                         'containers': containers}}) for container in containers]
        # SYNC_GROUPS.update({name: {'timeout': timeout, 'containers': containers}})


def connection_protocol():
    return dict([(k, Client(**v)) for k, v in CONTAINER[utils.get_container_info().container].items()])