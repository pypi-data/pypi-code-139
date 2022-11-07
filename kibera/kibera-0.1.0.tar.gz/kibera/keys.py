import logging
import re
from base64 import b64decode
from datetime import datetime
from multiprocessing.sharedctypes import Value
from urllib.parse import parse_qsl, urlparse

from kibera.core import db
from kibera.core.metrics import key_requests_total

logger = logging.getLogger(__name__)


class KeyParseError(Exception):
    pass

class KeyExistsError(Exception):
    pass


def get_random_key():
    key_requests_total.inc()

    keys = db.keys.find({}, {"_id": 0}).sort("serveCount", 1).limit(1)
    keys = list(keys)
    if len(keys) == 0:
        return None
    key = keys[0]
    db.keys.update_one(
        {"host": key["host"], "port": key["port"]}, {"$inc": {"serveCount": 1}}
    )
    return key


def get_key(query):
    return db.keys.find_one(query, {"_id": 0})


def list_keys(query):
    return db.keys.find(query, {"_id": 0})


def create_key(user, key_data):
    host, port = key_data["host"], key_data["port"]
    if host is None or port is None:
        raise KeyParseError("Key must have 'host' and 'port'")

    now = datetime.utcnow().replace(microsecond=0)

    key = get_key({"host": host, "port": port})
    if key is not None:
        raise KeyExistsError("Key with host and port already exists")

    db.keys.insert_one(
        {**key_data, "createdAt": now, "createdBy": user, "serveCount": 0},
    )

    logger.info(f"Created key {host}:{port} by {user}")


def update_key(user, key_data):
    host, port = key_data["host"], key_data["port"]
    if host is None or port is None:
        raise KeyParseError("Need to specify 'host' and 'port' when updating key")

    now = datetime.utcnow().replace(microsecond=0)
    db.keys.update_one(
        {"host": host, "port": port},
        {"$set": {**key_data, "updatedAt": now, "updatedBy": user}},
    )

    logger.info(f"Updated key {host}:{port} by {user}")


def delete_key(user, key_data):
    host, port = key_data["host"], key_data["port"]
    if host is None or port is None:
        raise KeyParseError("Need to specify 'host' and 'port' when deleting key")

    db.keys.delete_one({"host": host, "port": port})

    logger.info(f"Deleted key {host}:{port} by {user}")


def parse_key_url(url):
    if "://" not in url:
        url = "ss://" + url

    key = {}
    p = urlparse(url)

    if p.scheme != "ss":
        raise KeyParseError(f"Unsupported key scheme '{p.scheme}'")

    m = re.match("(?:([^@]+)[@])?([^:]+)(?:[:]([0-9]+))?", p.netloc)
    if m is None:
        raise KeyParseError(f"Invalid key '{url}'")

    ciphersecret, host, port = m.groups()
    if host is not None:
        key["host"] = host
    if port is not None:
        key["port"] = int(port)

    if ciphersecret is not None:
        if ":" not in ciphersecret:
            ciphersecret = str(b64decode(ciphersecret + "==="))
        if ":" not in ciphersecret:
            raise KeyParseError(f"Invalid cipher and secret in key '{url}'")
        key["cipher"], key["secret"] = ciphersecret.split(":")

    if p.fragment:
        key["name"] = p.fragment

    if p.query:
        key["param"] = (dict(parse_qsl(p.query)),)

    return key


def print_key(key):
    from rich import print_json

    print_json(data=key, sort_keys=True, default=str)
