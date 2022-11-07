from datetime import datetime
from sentimod.data._twitter import TwitterAPI
from sentimod.preprocessing._twitter import cleaner
# from sentimod.models._polarity import polarity_blob
from sentimod.models._huggingface import roberta_pol
from sentimod.data._google import google_trend
import pandas as pd


class Sentiment:
    def __init__(self) -> None:
        pass

    def get_sentiment(
        self,
        phrase: str,
        from_t: datetime,
        num: int,
    ) -> pd.DataFrame:
        """get sentiment of tweets with date

        Args:
            phrase (str): _description_
            from_t (datetime): _description_
            num (int): _description_

        Returns:
            pd.DataFrame: _description_
        """
        tweets = TwitterAPI.fetch_by_content(phrase, num, from_t)
        clean = cleaner(tweets)
        sent = roberta_pol(clean)
        return sent

    def get_trend(self, phrase: str, period: str = "now 7-d") -> pd.DataFrame:
        """get google trends for the specified time

        Args:
            phrase (str): _description_
            period (str, optional): _description_. Defaults to "now 7-d".

        Returns:
            pd.DataFrame: _description_
        """
        trends = google_trend(phrase, period)
        trends["Date"] = pd.to_datetime(trends["Date"])
        return trends
