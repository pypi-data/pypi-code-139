import functools
import logging
import re
import secrets
import string
from base64 import b64decode
from datetime import datetime
from multiprocessing.sharedctypes import Value
from urllib.parse import parse_qsl, urlparse

from flask import Flask, request
from werkzeug.exceptions import Unauthorized

from kibera.core import db

logger = logging.getLogger(__name__)

api_key_space = alphabet = string.ascii_letters + string.digits


class UserError(Exception):
    pass


def authenticate(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        api_key = None
        if request.data:
            api_key = request.json.get("api_key", None)
        if api_key is None:
            api_key = request.headers.get("api-key", None)
        if api_key is None:
            raise Unauthorized("Please provide an API key")
        user = db.users.find_one({"apiKey": api_key})
        if user is None:
            logger.warning("Auth attempted with invalid key: %s", api_key)
            raise Unauthorized("API key is invalid")
        logger.debug("User auth accepted: %s", user["name"])
        return func(user["name"], *args, **kwargs)

    return decorator


def create(name):
    user = db.users.find_one({"name": name})
    if user is not None:
        raise UserError("User already exists")

    user = {
        "name": name,
        "apiKey": "".join(secrets.choice(api_key_space) for i in range(32)),
    }
    db.users.insert_one(user)
    return user


def get(name):
    return db.users.find_one({"name": name}, {"_id": 0})


def list():
    return db.users.find({}, {"_id": 0})


def print_user(user):
    from rich import print_json

    print_json(data=user, sort_keys=True, default=str)
