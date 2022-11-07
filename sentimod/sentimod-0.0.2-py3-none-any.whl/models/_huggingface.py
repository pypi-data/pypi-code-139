import pandas as pd
import requests

model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
hf_token = "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"


def roberta_pol(content: pd.DataFrame) -> pd.DataFrame:
    """polarity score and label by roberta_pol

    Args:
        content (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    polarity = [0] * len(content)
    polarity = analysis(content["Clean"].values.tolist())
    content["Polarity"] = polarity
    return content


def analysis(
    data: list[str], model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
):
    """sentiment analysis by the chosen model

    Args:
        data (str): _
        model (_type_, optional): _. Defaults to "cardiffnlp/twitter-roberta-base-sentiment-latest":str.

    Returns:
        json: _
    """
    API_URL = "https://api-inference.huggingface.co/models/" + model
    headers = {"Authorization": "Bearer %s" % (hf_token)}
    payload = dict(inputs=data, options=dict(wait_for_model=True))
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
