import os
import requests


def get_token(url_path):
    from metaflow.metaflow_config import METADATA_SERVICE_HEADERS, from_conf
    from metaflow.exception import MetaflowException

    authServer = from_conf("OBP_AUTH_SERVER", "auth.obp.dev.outerbounds.xyz")
    assert url_path.startswith("/")
    url = "https://" + authServer + url_path
    headers = METADATA_SERVICE_HEADERS
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        token_info = r.json()
        return token_info

    except requests.exceptions.HTTPError as e:
        raise MetaflowException(repr(e))
