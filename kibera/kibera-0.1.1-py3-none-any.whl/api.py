import logging
import re

from flask import Flask, g, request
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Unauthorized

from kibera import keys
from kibera.core import db
from kibera.users import authenticate

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.before_request
def gather_request_data():
    g.method = request.method
    g.url = request.url


@app.after_request
def log_details(response):
    g.status = response.status_code
    logger.debug(f"{g.method} {g.url} {g.status}")
    return response


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return {"message": e.description}, 400


@app.route("/", methods=["GET"])
def get_random_key():
    key = keys.get_random_key()
    if key is None:
        return {}, NotFound
    return strip_key(key), 200


@app.route("/keys/", methods=["POST"])
@authenticate
def create_key(user):
    data = validate_key_data(request.json)
    try:
        keys.create_key(user, data)
    except keys.KeyExistsError:
        raise BadRequest("Key with given host and port already exists")
    return keys.get_key(data), 200


@app.route("/keys/", methods=["GET"])
@authenticate
def list_keys(user):
    data = validate_key_data(request.args, check_host_port=False)
    return list(keys.list_keys(data)), 200


@app.route("/key/<key>/", methods=["POST", "PUT"])
@app.route("/keys/<key>/", methods=["POST", "PUT"])
@authenticate
def update_key(user, key):
    data = keys.parse_key_url(key)
    data.update(request.json)
    data = validate_key_data(data)
    if keys.update_key(user, data):
        return keys.get_key(data), 200
    raise NotFound("Key not found")


@app.route("/key/<key>/", methods=["DELETE"])
@app.route("/keys/<key>/", methods=["DELETE"])
@authenticate
def delete_key(user, key):
    data = keys.parse_key_url(key)
    data = validate_key_data(data)
    keys.delete_key(user, data)
    return {"message": "Key deleted"}, 200


@app.route("/key/<key>/", methods=["GET"])
@app.route("/keys/<key>/", methods=["GET"])
@authenticate
def get_key(user, key):
    data = keys.parse_key_url(key)
    data.update(request.args)
    data = validate_key_data(data)
    k = keys.get_key(data)
    if k is None:
        raise NotFound(f"Key not found")
    return k, 200


def validate_key_data(data, check_host_port=True):
    if check_host_port:
        for k in ["port", "host"]:
            if not data.get(k):
                raise BadRequest(f"Missing field '{k}' in key data")
    if "port" in data:
        if type(data["port"]) is str and not data["port"].isnumeric():
            raise BadRequest(f"Invalid port {data['port']}")
        data["port"] = int(data["port"])
    return data


def strip_key(key):
    return {k: key.get(k) for k in ["host", "port", "cipher", "secret", "name"]}
