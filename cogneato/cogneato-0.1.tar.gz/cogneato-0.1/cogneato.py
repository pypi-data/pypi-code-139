"""
API for Cogneato, an experimental optimizer.
Optimize noisy metrics over continuous, categorical, and ordinal parameters.

See:
 https://cogneato.xyz
 https://github.com/cogneato-xyz/cogneato-api
"""

__version__ = "0.1"

import time
from dataclasses import dataclass
import requests
import pandas as pd


@dataclass
class _CogneatoResponse:
    df_analysis: pd.DataFrame
    df_design: pd.DataFrame
    message: str


def request(df_measurements, number_of_arms, url=None, num_retries=3):
    if url is None:
        url = "https://cogneato.xyz/api"

    df_text = df_measurements.to_json()
    d = {
        "number_of_arms": number_of_arms,
        "measurements": df_text,
    }

    for _ in range(num_retries):
        res = requests.post(url, "", json=d)
        if res.status_code != 200:
            time.sleep(3)
        else:
            break
    else:
        raise Exception(f"Request failed code = {res.status_code}")

    d = res.json()
    if "message" not in d:
        raise Exception(f"Invalid response {d}")
    if d["message"] != "Ok":
        raise Exception(d["message"])
    df_analysis = pd.read_json(d["analysis"])
    df_design = pd.read_json(d["design"])
    return _CogneatoResponse(df_analysis, df_design, d["message"])
