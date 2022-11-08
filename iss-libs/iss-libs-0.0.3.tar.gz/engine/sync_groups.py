import os
import re
import time
from engine import logger as log
from engine import utils
from engine import conn
from engine import redis_lib


RDB = redis_lib.RDB


class Structure:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def sync_group(group_name, timeout=None):
    if name:= get_sync_groups_name() or get_sync_container_name():
        group = f"{name}|{group_name}"
        log.info(f"Sync Group Name = {name}")
        log.info(f"Sync Cont List  = {list(RDB.hkeys(name))}")
        RDB.sadd(group, utils.get_variable('${slot_location}'))
        with utils.Timeout(timeout, 'Timeout Sync Group'):
            while not (RDB.scard(group) <= 0 or RDB.scard(group) == len(RDB.hkeys(name))):
                time.sleep(1)
        RDB.delete(group)
        return True
    utils.fail('ERROR: Missing Sync Group Name. Please Check file config.')


def add_sync_containers():
    slot = utils.get_variable('${slot_location}')
    sync = get_sync_container()
    s_sync = get_sync_groups()
    [RDB.delete(key) for key in RDB.keys('*') if sync.name in key]
    [[RDB.delete(key) for key in RDB.keys('*') if i in key] for i in list(s_sync)]

    time.sleep(sync.timeout)

    RDB.hset(sync.name, slot, utils.get_variable('${Raw_logs_path}'))
    [RDB.hset(i, slot, utils.get_variable('${Raw_logs_path}')) for i in list(s_sync)]

    with utils.TimeIt() as t:
        while t.duration <= int(sync.timeout):
            if len(RDB.hgetall(sync.name)) == len(sync.containers) and \
                    all([len(RDB.hgetall(i)) == len(s_sync[i]['containers']) for i in list(s_sync)]):
                break

    log.message('*' * 100)
    log.message(f"Cont Sync Group   : ['{sync.name}']")
    log.message(f'Cont Sync List    : {RDB.hkeys(sync.name)}')
    log.message(f'Cont Sync Path    : {RDB.hvals(sync.name)}')
    log.message(f'Cont Sync Time Out: {sync.timeout}')
    log.message('*' * 100)
    for i in list(s_sync):
        log.message(f"Super Cont Sync Group   : ['{i}']")
        log.message(f'Super Cont Sync List    : {RDB.hkeys(i)}')
        log.message(f'Super Cont Sync Path    : {RDB.hvals(i)}')


def get_sync_groups():
    return conn.SUPER_SYNC_GROUPS


def get_sync_groups_name():
    return ''.join(list(conn.SUPER_SYNC_GROUPS))


def get_sync_container():
    sync = conn.SYNC_GROUPS[utils.get_variable('${slot_location}')]
    return Structure(**sync)


def get_sync_container_name():
    return get_sync_container().name


def get_running_sync_containers():
    return RDB.hkeys(get_sync_container().name)
