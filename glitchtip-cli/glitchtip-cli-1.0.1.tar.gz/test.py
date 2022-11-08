# pylint: disable = missing-module-docstring, missing-function-docstring, missing-timeout
import responses
import requests
from responses import matchers

@responses.activate
def test_calc_api():
    responses.post(
        url="http://example.com/",
        body="one",
        match=[
            matchers.json_params_matcher({"page": {"name": "first", "type": "json"}})
        ],
    )
    resp = requests.request(
        "POST",
        "http://example.com/",
        headers={"Content-Type": "application/json"},
        json={"page": {"name": "first", "type": "json"}},
    )
    assert resp.status_code == 200
